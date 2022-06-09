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
            data = re.sub(
                r"Microsoft\ Windows\ \[version .+\]\r?\nCopyright.*(\r?\n)+[A-Z]\:.+?\>", 
                "", 
                data.decode("utf-8", "ignore")
            )
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
            self.__logger.warning(
                f"\n\nCommand Not Found: {command} returned exit code {return_code}: \nErrors: "
                f"{self.clean_output(errors)}/nOutput: {output}"
            )
            return return_dict
        if output or errors:
            if output:
                return_dict['output'] = self.clean_output(output)
                self.__logger.info(f"\n\nOutput: {return_dict['output']}")
            else:
                self.__logger.warning(
                    f"\n\nCommand: {command} returned exit code {return_code}: \n{self.clean_output(errors)}"
                )
        else:
            self.__logger.info("(No output)")
        return return_dict

    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _run(self, command, executor=None, host=None, cwd=None, elevation_required=False):
        raise NotImplementedError
