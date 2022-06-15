import os
import subprocess

from .runner import Runner
from ..base import Base
from ..frameworks.emulation import CapturedOutput


class LocalRunner(Runner):
    """Runs an AtomicTest or EmulationPhase objects locally."""

    def __init__(self, test, test_path):
        """A single AtomicTest or EmulationPhase object is provided and ran on the local system.

        Args:
            atomic_test (AtomicTest or EmulationPhase): A single AtomicTest or EmulationPhase object.
            test_path (Atomic or Adversary): A path where the AtomicTest or Adversary object resides
        """
        from ..frameworks import AtomicTest, EmulationPhase

        if isinstance(test, AtomicTest) or isinstance(test, EmulationPhase):
            self.test = test
            self.test_path = test_path
            self._type = str(test.__class__.__name__)
            self.__local_system_platform = self.get_local_system_platform()
        else:
            raise AttributeError(f"The provided test object is not one of 'AtomicTest' or 'EmulationPhase'. Exiting...")

    def _run(self, command, executor=None, host=None, cwd=None, elevation_required=False):
        p = subprocess.Popen(
            executor, 
            shell=False, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, 
            env=os.environ, 
            cwd=cwd
        )
        try:
            outs, errs = p.communicate(
                bytes(command, "utf-8") + b"\n", 
                timeout=Runner.CONFIG.command_timeout
            )
            # add to captured output here
            response = {
                "out": outs,
                "returncode": p.returncode,
                "errors": errs
            }
            self.print_process_output(command, p.returncode, outs, errs)
            return response
        except subprocess.TimeoutExpired as e:
            # Display output if it exists.
            if e.output:
                self.__logger.warning(e.output)
            if e.stdout:
                self.__logger.warning(e.stdout)
            if e.stderr:
                self.__logger.warning(e.stderr)
            self.__logger.warning("Command timed out!")

            # Kill the process.
            p.kill()
            return {}

    def _run_dependencies(self, host=None, executor=None):
        """Checking and running dependencies."""
        if self.test.dependency_executor_name:
            executor = self.test.dependency_executor_name
        for dependency in self.test.dependencies:
            self.__logger.debug(f"Dependency description: {dependency.description}")
            if Base.CONFIG.check_prereqs and dependency.prereq_command:
                self.__logger.debug("Running prerequisite command")
                command = dependency.get_check_prereqs_command(
                    executor=executor,
                    input_arguments=self.test.input_arguments,
                    elevation_required=self.test.elevation_required
                )
                response = self._run(
                    command=command,
                    executor=executor,
                    host=host
                )
                dependency.prereq_command_output = CapturedOutput(**response)

            if Base.CONFIG.get_prereqs and dependency.get_prereq_command:
                self.__logger.debug(f"Retrieving prerequistes")
                command = dependency.get_get_prereqs_command(
                    executor=executor,
                    input_arguments=self.test.input_arguments,
                    elevation_required=self.test.elevation_required
                )
                response = self.run(
                    command=command,
                    executor=executor,
                    host=host
                )
                dependency.get_prereq_command_output = CapturedOutput(**response)

    def execute(self):
        if self._type == 'EmulationPhase':
            executor = self.COMMAND_MAP.get(self.test.platforms._executor).get(self.test._platform)
            # now lets get the actual test/phase command
            command = getattr(
                getattr(self.test.platforms, self.test._platform), 
                self.test.platforms._executor
            )
            if not Base.CONFIG.check_prereqs and not Base.CONFIG.get_prereqs and not Base.CONFIG.cleanup:
                response = self._run(
                    command=command.get_command(executor_name=executor, input_arguments=self.test.input_arguments),
                    executor=executor
                )
                command.command_output = CapturedOutput(**response)
            elif Base.CONFIG.check_prereqs or Base.CONFIG.get_prereqs:
                if self.test.dependencies:
                    self._run_dependencies(executor=executor)
            elif Base.CONFIG.cleanup:
                cleanup_command = command.get_cleanup_command(
                    executor_name=executor,
                    input_arguments=self.test.input_arguments
                )
                if command:
                    response = self._run(
                        command=cleanup_command,
                        executor=executor
                    )
                    command.cleanup_output = CapturedOutput(**response)
        elif self._type == 'AtomicTest':
            if not Base.CONFIG.check_prereqs and not Base.CONFIG.get_prereqs and not Base.CONFIG.cleanup:
                self.__logger.info("Running defined atomic test command now.")
                executor = self.COMMAND_MAP.get(self.test.executor.name).get(self.__local_system_platform)
                response = self._run(
                    command=self.test.executor.get_command(self.test.input_arguments),
                    executor=executor
                )
                self.test.executor.captured_output = CapturedOutput(**response)
            elif Base.CONFIG.check_prereqs or Base.CONFIG.get_prereqs:
                if self.test.dependencies:
                    self._run_dependencies(executor=executor)
            elif Base.CONFIG.cleanup:
                cleanup_command = self.test.executor.get_cleanup_command(
                    executor_name=executor,
                    input_arguments=self.test.input_arguments
                )
                if cleanup_command:
                    response = self._run(
                        command=cleanup_command,
                        executor=executor
                    )
                    self.test.executor.cleanup_output = CapturedOutput(**response)
