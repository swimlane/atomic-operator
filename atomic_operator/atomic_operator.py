import os
import inspect

from .base import Base
from .models import (
    Config
)
from .configparser import ConfigParser
from .utils.exceptions import (
    AtomicsFolderNotFound,
    IncorrectParameters
)
from .execution import (
    LocalRunner,
    RemoteRunner,
    AWSRunner
)


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
                      password: UR4Swimlane!
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

    __test_responses = {}

    def __find_path(self, value):
        """Attempts to find a path containing the atomic-red-team repository

        Args:
            value (str): A starting path to iterate through

        Returns:
            str: An absolute path containing the path to the atomic-red-team repo
        """
        if value == os.getcwd():
            for x in os.listdir(value):
                if os.path.isdir(x) and 'redcanaryco-atomic-red-team' in x:
                    if os.path.exists(self.get_abs_path(os.path.join(x, 'atomics'))):
                        return self.get_abs_path(os.path.join(x, 'atomics'))
        else:
            if os.path.exists(self.get_abs_path(value)):
                return self.get_abs_path(value)

    def __check_arguments(self, kwargs, method):
        if kwargs:
            for arguments in inspect.getfullargspec(method):
                if isinstance(arguments, list):
                    for arg in arguments:
                        for key,val in kwargs.items():
                            if key in arg:
                                return IncorrectParameters(f"You passed in an argument of '{key}' which is not recognized. Did you mean '{arg}'?")
            return IncorrectParameters(f"You passed in an argument of '{key}' which is not recognized.")

    def __run_technique(self, technique, **kwargs):
        """This method is used to run defined Atomic tests within 
           a MITRE ATT&CK Technique.

        Args:
            technique (Atomic): An Atomic object which contains a list of AtomicTest
                                objects.
        """
        self.__logger.debug(f"Checking technique {technique.attack_technique} ({technique.display_name}) for applicable tests.")
        for test in technique.atomic_tests:
            self._set_input_arguments(test, **kwargs)
            if test.auto_generated_guid not in self.__test_responses:
                self.__test_responses[test.auto_generated_guid] = {}
            if technique.hosts:
                for host in technique.hosts:
                    self.__logger.info(f"Running {test.name} test ({test.auto_generated_guid}) for technique {technique.attack_technique}")
                    self.__logger.debug(f"Description: {test.description}")
                    if test.executor.name in ['sh', 'bash']:
                        self.__test_responses[test.auto_generated_guid].update(
                            RemoteRunner(test, technique.path).start(host=host, executor='ssh')
                        )
                    elif test.executor.name in ['command_prompt']:
                        self.__test_responses[test.auto_generated_guid].update(
                            RemoteRunner(test, technique.path).start(host=host, executor='cmd')
                        )
                    elif test.executor.name in ['powershell']:
                        self.__test_responses[test.auto_generated_guid].update(
                            RemoteRunner(test, technique.path).start(host=host, executor='powershell')
                        )
                    else:
                        self.__logger.warning(f"Unable to execute test since the executor is {test.executor.name}. Skipping.....")
            else:
                if self._check_platform(test, show_output=True):
                    self.__logger.info(f"Running {test.name} test ({test.auto_generated_guid}) for technique {technique.attack_technique}")
                    self.__logger.debug(f"Description: {test.description}")
                    if self._check_if_aws(test):
                        self.__test_responses[test.auto_generated_guid].update(
                            AWSRunner(test, technique.path).start()
                        )
                    else:
                        self.__test_responses[test.auto_generated_guid].update(
                            LocalRunner(test, technique.path).start()
                        )
            if self.__test_responses.get(test.auto_generated_guid):
                self.__test_responses[test.auto_generated_guid].update({
                    'technique_id': technique.attack_technique,
                    'technique_name': technique.display_name
                })

    def help(self, method=None):
        from fire.trace import FireTrace
        from fire.helptext import HelpText
        obj = AtomicOperator if not method else getattr(self, method)
        return HelpText(self.run,trace=FireTrace(obj))

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
        desintation = kwargs.pop('destination') if kwargs.get('destination') else desintation
        folder_name = self.download_atomic_red_team_repo(
            save_path=desintation, 
            **kwargs
        )
        return os.path.join(desintation, folder_name)

    def run(self, techniques: list=['all'], test_guids: list=[], select_tests=False,
                  atomics_path=os.getcwd(), check_prereqs=False, get_prereqs=False, 
                  cleanup=False, copy_source_files=True,command_timeout=20, debug=False, 
                  prompt_for_input_args=False, return_atomics=False, config_file=None, 
                  config_file_only=False, hosts=[], username=None, password=None, 
                  ssh_key_path=None, private_key_string=None, verify_ssl=False, 
                  ssh_port=22, ssh_timeout=5, *args, **kwargs) -> None:
        """The main method in which we run Atomic Red Team tests.

        Args:
            techniques (list, optional): One or more defined techniques by attack_technique ID. Defaults to 'all'.
            test_guids (list, optional): One or more Atomic test GUIDs. Defaults to None.
            select_tests (bool, optional): Select one or more tests from provided techniques. Defaults to False.
            atomics_path (str, optional): The path of Atomic tests. Defaults to os.getcwd().
            check_prereqs (bool, optional): Whether or not to check for prereq dependencies (prereq_comand). Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            copy_source_files (bool, optional): Whether or not you want to copy any related source (src, bin, etc.) files to a remote host. Defaults to True.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            debug (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            return_atomics (bool, optional): Whether or not you want to return atomics instead of running them. Defaults to False.
            config_file (str, optional): A path to a conifg_file which is used to automate atomic-operator in environments. Default to None.
            config_file_only (bool, optional): Whether or not you want to run tests based on the provided config_file only. Defaults to False.
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
        response = self.__check_arguments(kwargs, self.run)
        if response:
            return response
        if kwargs.get('help'):
            return self.help(method='run')
        if debug:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
        count = 0
        if check_prereqs:
            count += 1
        if get_prereqs:
            count += 1
        if cleanup:
            count += 1
        if count > 1:
            return IncorrectParameters(f"You have passed in incompatible arguments. Please only provide one of 'check_prereqs','get_prereqs','cleanup'.")
        atomics_path = self.__find_path(atomics_path)
        if not atomics_path:
            return AtomicsFolderNotFound('Unable to find a folder containing Atomics. Please provide a path or run get_atomics.')
        Base.CONFIG = Config(
            atomics_path          = atomics_path,
            check_prereqs         = check_prereqs,
            get_prereqs           = get_prereqs,
            cleanup               = cleanup,
            command_timeout       = command_timeout,
            debug                 = debug,
            prompt_for_input_args = prompt_for_input_args,
            kwargs                = kwargs,
            copy_source_files     = copy_source_files
        )
        # taking inputs from both config_file and passed in values via command
        # line to build a run_list of objects
        self.__config_parser = ConfigParser(
                config_file=config_file,
                techniques=None if config_file_only else self.parse_input_lists(techniques),
                test_guids=None if config_file_only else self.parse_input_lists(test_guids),
                host_list=None if config_file_only else self.parse_input_lists(hosts),
                username=username,
                password=password,
                ssh_key_path=ssh_key_path,
                private_key_string=private_key_string,
                verify_ssl=verify_ssl,
                ssh_port=ssh_port,
                ssh_timeout=ssh_timeout,
                select_tests=select_tests
            )
        self.__run_list = self.__config_parser.run_list

        __return_atomics = []
        for item in self.__run_list:
            if return_atomics:
                __return_atomics.append(item)
            elif kwargs.get('kwargs'):
                self.__run_technique(item, **kwargs.get('kwargs'))
            else:
                self.__run_technique(item)
        if return_atomics and __return_atomics:
            return __return_atomics
        return self.__test_responses
