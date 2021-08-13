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

    def __run_test(self, technique, **kwargs):
        self.__logger.info(f"Running tests for technique {technique.attack_technique} ({technique.display_name})")
        for test in technique.atomic_tests:
            if test.supported_platforms and self.get_local_system_platform() in test.supported_platforms:
                args_dict = kwargs
                if Base.CONFIG.prompt_for_input_args:
                    for input in test.input_arguments:
                        args_dict[input.name] = self.prompt_user_for_input(test.name, input)
                test.set_command_inputs(**args_dict)
                self.__logger.info(f"Running {test.name} test")
                self.show_details(f"Description: {test.description}")
                LocalRunner(test, technique.path).run()

    def get_atomics(self, desintation=os.getcwd()):
        if not os.path.exists(desintation):
            os.makedirs(desintation)
        folder_name = self.download_atomic_red_team_repo(desintation)
        return os.path.join(desintation, folder_name)

    def run(
        self, 
        techniques: list=['All'], 
        atomics_path=os.getcwd(), 
        check_dependencies=False, 
        get_prereqs=False, 
        cleanup=False, 
        command_timeout=20, 
        show_details=False,
        prompt_for_input_args=False,
        **kwargs):
        """The main method in which we run Atomic Red Team tests.

        Args:
            techniques (list, optional): One or more defined techniques by attack_technique ID. Defaults to 'All'.
            atomics_path (str, optional): The path of Atomic tests. Defaults to os.getcwd().
            check_dependencies (bool, optional): Whether or not to check for dependencies. Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            show_details (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            kwargs (dict, optional): If provided, keys matching inputs for a test will be replaced. Default is None.

        Raises:
            ValueError: If a provided technique is unknown we raise an error.
        """
        if not isinstance(techniques, list):
            techniques = [t.strip() for t in techniques.split(',')]
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
                        self.__run_test(self.__techniques[technique], **kwargs.get('kwargs'))
                    else:
                        self.__run_test(self.__techniques[technique])
                    pass
                else:
                    raise ValueError(f"Unable to find technique {technique}")
        elif 'All' in techniques:
            # process all techniques
            for key,val in self.__techniques.items():
                self.__run_test(val)
