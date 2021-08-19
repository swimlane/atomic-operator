import os
from .base import Base
from .config import Config
from .atomic.loader import Loader
from .execution.localrunner import LocalRunner


class AtomicOperator(Base):

    """Main class used to run Atomic Red Team tests.

    atomic-operator is used to run Atomic Red Team tests both locally and remotely.
    These tests (atomics) are predefined tests to mock or emulate a specific technique.

    Raises:
        ValueError: If a provided technique is unknown we raise an error.
    """

    __techniques = None

    def __run_technique(self, technique, **kwargs):
        self.__logger.info(f"Running tests for technique {technique.attack_technique} ({technique.display_name})")
        for test in technique.atomic_tests:
            if test.supported_platforms and self.get_local_system_platform() in test.supported_platforms:
                args_dict = kwargs if kwargs else {}
                if self.config_file:
                    if self.config_file.get(test.auto_generated_guid):
                        if self.config_file[test.auto_generated_guid]:
                            args_dict.update(self.config_file[test.auto_generated_guid])
                        test.set_command_inputs(**args_dict)
                        self.__logger.info(f"Running {test.name} test")
                        self.show_details(f"Description: {test.description}")
                        LocalRunner(test, technique.path).run()
                else:
                    if Base.CONFIG.prompt_for_input_args:
                        for input in test.input_arguments:
                            args_dict[input.name] = self.prompt_user_for_input(test.name, input)
                    test.set_command_inputs(**args_dict)
                    self.__logger.info(f"Running {test.name} test")
                    self.show_details(f"Description: {test.description}")
                    if self.test_guids:
                        if test.auto_generated_guid in self.test_guids:
                            LocalRunner(test, technique.path).run()
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

    def run(
        self, 
        techniques: list=['All'], 
        test_guids: list=[],
        atomics_path=[os.path.join(os.getcwd(), x, 'atomics') for x in os.listdir(os.getcwd()) if 'redcanaryco-atomic-red-team' in x][0], 
        check_dependencies=False, 
        get_prereqs=False, 
        cleanup=False, 
        command_timeout=20, 
        show_details=False,
        prompt_for_input_args=False,
        config_file=None,
        **kwargs):
        """The main method in which we run Atomic Red Team tests.

        config_file definition:
            atomic-operator's run method can be supplied with a path to a configuration file (config_file) which defines 
            specific tests and/or values for input parameters to facilitate automation of said tests.
            An example of this config_file can be seen below:

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

        Args:
            techniques (list, optional): One or more defined techniques by attack_technique ID. Defaults to 'All'.
            test_guids (list, optional): One or more Atomic test GUIDs. Defaults to None.
            atomics_path (str, optional): The path of Atomic tests. Defaults to [os.path.join(os.getcwd(), x, 'atomics') for x in os.listdir(os.getcwd()) if 'redcanaryco-atomic-red-team' in x][0].
            check_dependencies (bool, optional): Whether or not to check for dependencies. Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            show_details (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            config_file (str, optional): A path to a conifg_file which is used to automate atomic-operator in environments. Default to None.
            kwargs (dict, optional): If provided, keys matching inputs for a test will be replaced. Default is None.

        Raises:
            ValueError: If a provided technique is unknown we raise an error.
        """
        if not isinstance(techniques, list):
            techniques = [t.strip() for t in techniques.split(',')]
        self.test_guids = test_guids
        self.config_file = self.format_config_data(config_file)
        Base.CONFIG = Config(
            atomics_path          = atomics_path,
            check_dependencies    = check_dependencies,
            get_prereqs           = get_prereqs,
            cleanup               = cleanup,
            command_timeout       = command_timeout,
            show_details          = show_details,
            prompt_for_input_args = prompt_for_input_args
        )
        self.__techniques = Loader().load_techniques()
        iteration = 0
        if 'All' not in techniques:
            for technique in techniques:
                if self.__techniques.get(technique):
                    iteration += 1
                    if kwargs:
                        self.__run_technique(self.__techniques[technique], **kwargs.get('kwargs'))
                    else:
                        self.__run_technique(self.__techniques[technique])
                    pass
                else:
                    raise ValueError(f"Unable to find technique {technique}")
        elif 'All' in techniques:
            # process all techniques
            for key,val in self.__techniques.items():
                if kwargs:
                    self.__run_technique(val, **kwargs.get('kwargs'))
                else:
                    self.__run_technique(val)
