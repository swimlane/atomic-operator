import os
import subprocess
from .runner import Runner


class LocalRunner(Runner):
    """Runs AtomicTest objects locally
    """

    def __init__(self, atomic_test, test_path):
        """A single AtomicTest object is provided and ran on the local system

        Args:
            atomic_test (AtomicTest): A single AtomicTest object.
            test_path (Atomic): A path where the AtomicTest object resides
        """
        self.test = atomic_test
        self.test_path = test_path
        self.__local_system_platform = self.get_local_system_platform()

    def execute_process(self, command, executor=None, host=None, cwd=None):
        """Executes commands using subprocess

        Args:
            executor (str): An executor or shell used to execute the provided command(s)
            command (str): The commands to run using subprocess
            cwd (str): A string which indicates the current working directory to run the command

        Returns:
            tuple: A tuple of either outputs or errors from subprocess
        """
        command = self._replace_command_string(command, self.CONFIG.atomics_path, input_arguments=self.test.input_arguments)
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
            response = self.print_process_output(command, p.returncode, outs, errs)
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

    def _get_executor_command(self):
        """Checking if executor works with local system platform
        """
        __executor = None
        self.__logger.debug(f"Checking if executor works on local system platform.")
        if self.__local_system_platform in self.test.supported_platforms:
            if self.test.executor.name != 'manual':
                __executor = self.command_map.get(self.test.executor.name).get(self.__local_system_platform)
        return __executor

    def start(self):
        return self.execute(executor=self._get_executor_command())
