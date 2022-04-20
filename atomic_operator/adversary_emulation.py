import os
import inspect

from .base import Base
from .models import (
    Config
)
from .configparser import ConfigParser
from .utils.exceptions import (
    ContentFolderNotFound,
    IncorrectParameters
)
from .execution import (
    LocalRunner,
    RemoteRunner,
    AWSRunner
)


class AdversaryEmulationLibrary(Base):

    """Main class used to run Adversary Emulation plans.

    atomic-operator can used to run these emulation plans both locally and remotely.
    These plans (emulations) are predefined tests to mock or emulate a specific adversary.

    Raises:
        ValueError: If a provided technique is unknown we raise an error.
    """

    __test_responses = {}

    def __find_path(self, path: str, adversary: str):
        """Attempts to find a path containing the adversary-emulation-library repository

        Args:
            path (str): A starting path to iterate through
            adversary (str): A Adversary Emulation Plan adversary folder name

        Returns:
            str: An absolute path containing the path to the adversary-emulation-library repo
        """
        if path == os.getcwd():
            for x in os.listdir(path):
                if os.path.isdir(x) and 'center-for-threat-informed-defense-adversary_emulation_library' in x:
                    if os.path.exists(self.get_abs_path(os.path.join(x, adversary))):
                        return self.get_abs_path(x)
        else:
            if os.path.exists(self.get_abs_path(path)):
                return self.get_abs_path(path)

    def __check_arguments(self, kwargs, method):
        if kwargs:
            for arguments in inspect.getfullargspec(method):
                if isinstance(arguments, list):
                    for arg in arguments:
                        for key,val in kwargs.items():
                            if key in arg:
                                return IncorrectParameters(f"You passed in an argument of '{key}' which is not recognized. Did you mean '{arg}'?")
            return IncorrectParameters(f"You passed in an argument of '{key}' which is not recognized.")

    def __run_emulation(self, emulation, **kwargs):
        """This method is used to run defined Emulation Plans for an adversary.

        Args:
            emulation (EmulationPlanDetails): An Adversary Emulation Plan Details object which contains a list of plan phases.
        """
        self.__logger.debug(f"Attempting to run Emulation Plan phases for adversary '{emulation.adversary_name}'")
        for phase in emulation.phases:
            self._set_input_arguments(phase, **kwargs)
            if phase.id not in self.__test_responses:
                self.__test_responses[phase.id] = {}
            for executor in phase.executors:
                if emulation.hosts:
                    for host in emulation.hosts:
                        self.__logger.info(f"Running procedure group '{phase.procedure_group} (Step {phase.procedure_step}) for tactic {phase.tactic} and technique {phase.technique.name}")
                        self.__logger.debug(f"Description: {phase.description}")
                        if executor.name in ['sh', 'bash']:
                            self.__test_responses[phase.id].update(
                                RemoteRunner(phase, emulation.path).start(host=host, executor='ssh')
                            )
                        elif executor.name in ['command_prompt']:
                            self.__test_responses[phase.id].update(
                                RemoteRunner(phase, emulation.path).start(host=host, executor='cmd')
                            )
                        elif executor.name in ['powershell']:
                            self.__test_responses[phase.id].update(
                                RemoteRunner(phase, emulation.path).start(host=host, executor='powershell')
                            )
                        else:
                            self.__logger.warning(f"Unable to execute test since the executor is {executor.name}. Skipping.....")
                else:
                    if self._check_platform(phase, show_output=True):
                        self.__logger.info(f"Running {phase.name} test ({phase.id}) for technique {phase.technique.name}")
                        self.__logger.debug(f"Description: {phase.description}")
                        if self._check_if_aws(phase):
                            self.__test_responses[phase.id].update(
                                AWSRunner(phase, emulation.path).start()
                            )
                        else:
                            self.__test_responses[phase.id].update(
                                LocalRunner(phase, emulation.path).start()
                            )
            if self.__test_responses.get(phase.id):
                self.__test_responses[phase.id].update({
                    'technique_id': phase.technique.attack_id,
                    'technique_name': phase.technique.name
                })

    def help(self, method=None):
        from fire.trace import FireTrace
        from fire.helptext import HelpText
        obj = AdversaryEmulationLibrary if not method else getattr(self, method)
        return HelpText(self.run,trace=FireTrace(obj))

    def get_content(self, desintation=os.getcwd(), **kwargs):
        """Downloads the Adversary Emulation Plan repository to your local system.

        Args:
            desintation (str, optional): A folder path to download the repositorty data to. Defaults to os.getcwd().
            kwargs (dict, optional): This kwargs will be passed along to Python requests library during download. Defaults to None.

        Returns:
            str: The path the data can be found at.
        """
        if not os.path.exists(desintation):
            os.makedirs(desintation)
        desintation = kwargs.pop('destination') if kwargs.get('destination') else desintation
        self.__logger.info(f"Downloading content from GitHub repo.")
        folder_name = self.download_github_repo(
            save_path=desintation, 
            type='adversary-emulation',
            **kwargs
        )
        return os.path.join(desintation, folder_name)

    def run(self, adversary: str, content_path=os.getcwd(), check_prereqs=False, get_prereqs=False, 
                  cleanup=False, copy_source_files=True, command_timeout=20, debug=False, 
                  prompt_for_input_args=False, return_content=False, config_file=None, 
                  config_file_only=False, hosts=[], username=None, password=None, 
                  ssh_key_path=None, private_key_string=None, verify_ssl=False, 
                  ssh_port=22, ssh_timeout=5, *args, **kwargs) -> None:
        """The main method in which we run Adversary Emulation Plans.

        Args:
            adversary (str): One or more defined adversary emulation plans by their names
            content_path (str, optional): The path of Adversary Emulation Library tests. Defaults to os.getcwd().
            check_prereqs (bool, optional): Whether or not to check for prereq dependencies (prereq_comand). Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            copy_source_files (bool, optional): Whether or not you want to copy any related source (src, bin, etc.) files to a remote host. Defaults to True.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            debug (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            return_content (bool, optional): Whether or not you want to return adversary emulation plans instead of running them. Defaults to False.
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
            ValueError: If a provided adversary is unknown we raise an error.
            IncorrectParameters: Is raised when incompatible arguments are passed.
            ContentFolderNotFound: Is raised when atomic-operator is unable to find
                                   a folder containing content.
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
        content_path = self.__find_path(path=content_path, adversary=adversary)
        if not content_path:
            return ContentFolderNotFound('Unable to find a folder containing adversary emulation repository. Please provide a path or run get_content.')
        Base.CONFIG = Config(
            content_path          = content_path,
            check_prereqs         = check_prereqs,
            get_prereqs           = get_prereqs,
            cleanup               = cleanup,
            command_timeout       = command_timeout,
            debug                 = debug,
            prompt_for_input_args = prompt_for_input_args,
            kwargs                = kwargs,
            copy_source_files     = copy_source_files
        )
        self.__logger.info(f"Parsing config")
        # taking inputs from both config_file and passed in values via command
        # line to build a run_list of objects
        self.__config_parser = ConfigParser(
                config_file=config_file,
                adversary=adversary,
                host_list=None if config_file_only else self.parse_input_lists(hosts),
                username=username,
                password=password,
                ssh_key_path=ssh_key_path,
                private_key_string=private_key_string,
                verify_ssl=verify_ssl,
                ssh_port=ssh_port,
                ssh_timeout=ssh_timeout
            )
        self.__run_list = self.__config_parser.run_list

        __return_content = []
        for item in self.__run_list:
            if return_content:
                __return_content.append(item)
            elif kwargs.get('kwargs'):
                self.__run_emulation(item, **kwargs.get('kwargs'))
            else:
                self.__run_emulation(item)
        if return_content and __return_content:
            return __return_content
        return self.__test_responses
