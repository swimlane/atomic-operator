import os
from rudder import Host, Runner

from .base import Base
from .config import Config
from .parser import ConfigParser
from .atomic.loader import Loader
from .utils.exceptions import AtomicsFolderNotFound
from .execution.localrunner import LocalRunner
from .execution.remoterunner import RemoteRunner


class AtomicOperator(Base):

    """Main class used to run Atomic Red Team tests.

    atomic-operator is used to run Atomic Red Team tests both locally and remotely.
    These tests (atomics) are predefined tests to mock or emulate a specific technique.

    config_file definition:
            atomic-operator's run method can be supplied with a path to a configuration file (config_file) which defines 
            specific tests and/or values for input parameters to facilitate automation of said tests.
            An example of this config_file can be seen below:

                inventory:
                  linux1:
                    executor: ssh
                    authentication:
                      username: root
                      password: ***REMOVED***
                      #ssk_key_path:
                      port: 22
                      timeout: 5
                    hosts:
                      # - 192.168.1.1
                      - 10.32.100.199
                      # etc.
                atomic_tests:
                  - guid: f7e6ec05-c19e-4a80-a7e7-241027992fdb
                    input_arguments:
                      output_file:
                        value: custom_output.txt
                      input_file:
                        value: custom_input.txt
                  - guid: 3ff64f0b-3af2-3866-339d-38d9791407c3
                    input_arguments:
                      second_arg:
                        value: SWAPPPED argument
                  - guid: 32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2
                    inventories:
                      - linux1

    Raises:
        ValueError: If a provided technique is unknown we raise an error.
    """

    def __find_path(self, value):
        if value == os.getcwd():
            for x in os.listdir(value):
                if os.path.isdir(x) and 'redcanaryco-atomic-red-team' in x:
                    if os.path.exists(Base().get_abs_path(os.path.join(x, 'atomics'))):
                        return Base().get_abs_path(os.path.join(x, 'atomics'))
        else:
            if os.path.exists(Base().get_abs_path(value)):
                return Base().get_abs_path(value)

    def __show_unsupported_platform(self, test, show_output=False) -> None:
        output_string = f"You provided a test ({test.auto_generated_guid}) '{test.name}' which is not supported on this platform. Skipping..."
        if show_output:
            self.__logger.warning(output_string)
        else:
            self.show_details(output_string)

    def __check_platform(self, test, show_output=False) -> bool:
        if test.supported_platforms and self.get_local_system_platform() not in test.supported_platforms:
            self.__show_unsupported_platform(test, show_output=show_output)
            return False
        return True

    def __run_technique(self, technique, **kwargs) -> None:
        self.show_details(f"Checking technique {technique.attack_technique} ({technique.display_name}) for applicable tests.")
        for test in technique.atomic_tests:
            __should_run_test = False
            args_dict = kwargs if kwargs else {}
            if Base.CONFIG.prompt_for_input_args:
                for input in test.input_arguments:
                    args_dict[input.name] = self.prompt_user_for_input(test.name, input)
            if self.config_file:
                if self.config_file.is_defined(test.auto_generated_guid):
                    if self.__check_platform(test, show_output=True):
                        args_dict.update(self.config_file.get_inputs(test.auto_generated_guid))
                        __should_run_test = True
            if self.__test_guids and test.auto_generated_guid in self.__test_guids:
                if self.__check_platform(test, show_output=True):
                    __should_run_test = True
            if not self.config_file and not self.__test_guids:
                if self.__check_platform(test):
                    __should_run_test = True
            if __should_run_test:
                test.set_command_inputs(**args_dict)
                self.__logger.info(f"Running {test.name} test ({test.auto_generated_guid}) for technique {technique.attack_technique}")
                self.show_details(f"Description: {test.description}")
                if self.config_file:
                    remote_config = self.config_file.get_inventory(test.auto_generated_guid)
                    if remote_config:
                        RemoteRunner(test, technique.path, remote_config).run()
                elif self.__remote_hosts:
                    if 'macos' in test.supported_platforms or 'linux' in test.supported_platforms:
                        RemoteRunner(test, technique.path, [Runner(hosts=self.__remote_hosts, executor='ssh', command='')])
                    else:
                        RemoteRunner(test, technique.path, [Runner(hosts=self.__remote_hosts, executor=test.executor.name, command='')])
                else:
                    LocalRunner(test, technique.path).run()

    def get_atomics(self, desintation=os.getcwd(), **kwargs):
        """Downloads the RedCanary atomic-red-team repository to your local system.

        Args:
            desintation (str, optional): A folder path to download the repositorty data to. Defaults to os.getcwd().
            kwargs (dict, optional): This kwargs will be passed along to Python requests library during download. Defaults to None.

        Returns:
            str: The path the data can be found at.
        """
        if not os.path.exists(desintation):
            os.makedirs(desintation)
        folder_name = self.download_atomic_red_team_repo(desintation, **kwargs)
        return os.path.join(desintation, folder_name)

    def __create_remote_host_object(self, 
        hosts=[],
        username=None,
        password=None,
        ssh_key_path=None,
        private_key_string=None,
        verify_ssl=False,
        ssh_port=22,
        ssh_timeout=5):
            return_list = []
            if hosts:
                for host in hosts:
                    return_list.append(
                        Host(
                            hostname=host,
                            username=username,
                            password=password,
                            ssh_key_path=ssh_key_path,
                            private_key_string=private_key_string,
                            verify_ssl=verify_ssl,
                            port=ssh_port,
                            timeout=ssh_timeout
                        )
                    )
            return return_list

    def run(
        self, 
        techniques: list=['All'], 
        test_guids: list=[],
        atomics_path=os.getcwd(), 
        check_dependencies=False, 
        get_prereqs=False, 
        cleanup=False, 
        command_timeout=20, 
        show_details=False,
        prompt_for_input_args=False,
        return_atomics=False,
        config_file=None,
        hosts=[],
        username=None,
        password=None,
        ssh_key_path=None,
        private_key_string=None,
        verify_ssl=False,
        ssh_port=22,
        ssh_timeout=5,
        **kwargs) -> None:
        """The main method in which we run Atomic Red Team tests.

        Args:
            techniques (list, optional): One or more defined techniques by attack_technique ID. Defaults to 'All'.
            test_guids (list, optional): One or more Atomic test GUIDs. Defaults to None.
            atomics_path (str, optional): The path of Atomic tests. Defaults to os.getcwd().
            check_dependencies (bool, optional): Whether or not to check for dependencies. Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            show_details (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            return_atomics (bool, optional): Whether or not you want to return atomics instead of running them. Defaults to False.
            config_file (str, optional): A path to a conifg_file which is used to automate atomic-operator in environments. Default to None.
            hosts (list, optional): A list of one or more remote hosts to run a test on. Defaults to [].
            username (str, optional): Username for authentication of remote connections. Defaults to None.
            password (str, optional): Password for authentication of remote connections. Defaults to None.
            ssh_key_path (str, optional): Path to a SSH Key for authentication of remote connections. Defaults to None.
            private_key_string (str, optional): A private SSH Key string used for authentication of remote connections. Defaults to None.
            verify_ssl (bool, optional): Whether or not to verify ssl when connecting over RDP (windows). Defaults to False.
            ssh_port (int, optional): SSH port for authentication of remote connections. Defaults to 22.
            ssh_timeout (int, optional): SSH timeout for authentication of remote connections. Defaults to 5.
            kwargs (dict, optional): If provided, keys matching inputs for a test will be replaced. Default is None.

        Raises:
            ValueError: If a provided technique is unknown we raise an error.
        """
        if not isinstance(techniques, list):
            self._techniques = [t.strip() for t in techniques.split(',')]
        else:
            self._techniques = techniques
        if not isinstance(test_guids, list):
            self.__test_guids = set([t.strip() for t in test_guids.split(',')])
        else:
            self.__test_guids = set(test_guids)
        self.config_file = ConfigParser(config_file=config_file) if config_file else None
        self.__test_guids = list(self.__test_guids)
        self.__remote_hosts = self.__create_remote_host_object(
            hosts=hosts, 
            username=username, 
            password=password, 
            ssh_key_path=ssh_key_path, 
            verify_ssl=verify_ssl,
            private_key_string=private_key_string,
            ssh_port=ssh_port,
            ssh_timeout=ssh_timeout)
        atomics_path = self.__find_path(atomics_path)
        if not atomics_path:
            return AtomicsFolderNotFound('Unable to find a folder containing Atomics. Please provide a path or run get_atomics.')
        Base.CONFIG = Config(
            atomics_path          = atomics_path,
            check_dependencies    = check_dependencies,
            get_prereqs           = get_prereqs,
            cleanup               = cleanup,
            command_timeout       = command_timeout,
            show_details          = show_details,
            prompt_for_input_args = prompt_for_input_args
        )
        self.__loaded_techniques = Loader().load_techniques()
        __return_atomics = []
        if 'All' not in self._techniques:
            for technique in self._techniques:
                if self.__loaded_techniques.get(technique):
                    if return_atomics:
                        __return_atomics.append(self.__loaded_techniques[technique])
                    elif kwargs.get('kwargs'):
                        self.__run_technique(self.__loaded_techniques[technique], **kwargs.get('kwargs'))
                    else:
                        self.__run_technique(self.__loaded_techniques[technique])
                    pass
                else:
                    raise ValueError(f"Unable to find technique {technique}")
        elif 'All' in self._techniques:
            # process all techniques
            for key,val in self.__loaded_techniques.items():
                if return_atomics:
                    __return_atomics.append(val)
                elif kwargs.get('kwargs'):
                    self.__run_technique(val, **kwargs.get('kwargs'))
                else:
                    self.__run_technique(val)
        if return_atomics and __return_atomics:
            return __return_atomics
