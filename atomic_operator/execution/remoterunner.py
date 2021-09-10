from rudder import Rudder
from ..base import Base


class RemoteRunner(Base):
    
    def __init__(self, atomic_test, test_path, runner):
        """A single AtomicTest object is provided and ran on the local system

        Args:
            atomic_test (AtomicTest): A single AtomicTest object.
            test_path (Atomic): A path where the AtomicTest object resides
            runner (Runner): A Runner object defined with a config file
        """
        self.test = atomic_test
        self.test_path = test_path
        self.runner = runner

    def execute_remote_process(self, command, override_executor=None) -> None:
        """Main method to execute commands using Rudder

        Args:
            command (str): The command to run remotely on the desired systems
            override_executor (str, optional): An override executor that can be passed to rudder. Defaults to None.
        """
        for runner in self.runner:
            for response in Rudder().execute(
                host=runner.hosts,
                executor=override_executor if override_executor else runner.executor,
                command=command
            ):
                self.__logger.info(response)

    def __run_dependencies(self) -> None:
        """Checking dependencies
        """
        if self.test.dependency_executor_name:
            executor = self.test.dependency_executor_name
        for dependency in self.test.dependencies:
            self.show_details(f"Dependency description: {dependency.description}")
            if Base.CONFIG.get_prereqs:
                self.show_details(f"Retrieving prerequistes")
                self.execute_remote_process(dependency.get_prereq_command, override_executor=executor)
            self.execute_remote_process(dependency.prereq_command, override_executor=executor)

    def run(self) -> None:
        """The main method which runs a single AtomicTest object remotely on one or more defined hosts.
        """
        if Base.CONFIG.check_dependencies and self.test.dependencies:
            self.__run_dependencies()
        self.show_details("Running command")
        self.execute_remote_process(self.test.executor.command)
        if Base.CONFIG.cleanup and self.test.executor.cleanup_command:
            self.show_details("Running cleanup command")
            self.execute_remote_process(self.test.executor.cleanup_command)
