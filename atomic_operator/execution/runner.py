import re
import abc

from ..base import Base


class Runner(Base):

    def clean_output(self, data):
        """Decodes data and strips CLI garbage from returned outputs and errors

        Args:
            data (str): A output or error returned from subprocess

        Returns:
            str: A cleaned string which will be displayed on the console and in logs
        """
        if data:
            # Remove Windows CLI garbage
            data = re.sub(r"Microsoft\ Windows\ \[version .+\]\r?\nCopyright.*(\r?\n)+[A-Z]\:.+?\>", "", data.decode("utf-8", "ignore"))
            # formats strings with newline and return characters
            return re.sub(r"(\r?\n)*[A-Z]\:.+?\>", "", data)

    def print_process_output(self, command, return_code, output, errors):
        """Outputs the appropriate outputs if they exists to the console and log files

        Args:
            command (str): The command which was ran by subprocess
            return_code (int): The return code from subprocess
            output (bytes): Output from subprocess which is typically in bytes
            errors (bytes): Errors from subprocess which is typically in bytes
        """
        return_dict = {}
        if return_code == 127:
            return_dict['error'] =  f"\n\nCommand Not Found: {command} returned exit code {return_code}: \nErrors: {self.clean_output(errors)}/nOutput: {output}"
            self.__logger.warning(return_dict['error'])
            return return_dict
        if output or errors:
            if output:
                return_dict['output'] = self.clean_output(output)
                self.__logger.info("\n\nOutput: {}".format(return_dict['output']))
            else:
                return_dict['error'] =  f"\n\nCommand: {command} returned exit code {return_code}: \n{self.clean_output(errors)}"
                self.__logger.warning(return_dict['error'])
        else:
            self.__logger.info("(No output)")
        return return_dict

    def _run_dependencies(self, host=None, executor=None):
        """Checking dependencies
        """
        return_dict = {}
        if self.test.dependency_executor_name:
            executor = self.test.dependency_executor_name
        for dependency in self.test.dependencies:
            self.show_details(f"Dependency description: {dependency.description}")
            if Base.CONFIG.get_prereqs and dependency.get_prereq_command:
                self.show_details(f"Retrieving prerequistes")
                get_prereq_response = self.execute_process(
                    command=dependency.get_prereq_command,
                    executor=executor,
                    host=host
                )
                for key,val in get_prereq_response.items():
                    if key not in return_dict:
                        return_dict[key] = {}
                    return_dict[key].update({'get_prereqs': val})
            if Base.CONFIG.check_prereqs and dependency.prereq_command:
                response = self.execute_process(
                    command=dependency.prereq_command,
                    executor=executor,
                    host=host
                )
                for key,val in response.items():
                    if key not in return_dict:
                        return_dict[key] = {}
                    return_dict[key].update({'prereq_command': val})
        return return_dict

    def execute(self, host_name='localhost', executor=None, host=None):
        """The main method which runs a single AtomicTest object on a local system.
        """
        return_dict = {}
        self.show_details(f"Using {executor} as executor.")
        if executor:
            if Base.CONFIG.check_prereqs and self.test.dependencies:
                return_dict.update(self._run_dependencies(host=host, executor=executor))
            self.show_details("Running command")
            response = self.execute_process(
                command=self.test.executor.command,
                executor=executor,
                host=host,
                cwd=self.test_path
            )
            return_dict.update({'command': response})
            if Runner.CONFIG.cleanup and self.test.executor.cleanup_command:
                self.show_details("Running cleanup command")
                cleanup_response = self.execute_process(
                    command=self.test.executor.cleanup_command,
                    executor=executor,
                    host=host,
                    cwd=self.test_path
                )
                return_dict.update({'cleanup': cleanup_response})
        return {host_name: return_dict}

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute_process(self, command, executor=None, host=None, cwd=None):
        raise NotImplementedError
