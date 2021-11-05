import os
import sys
import zipfile
from io import BytesIO
import platform
import requests
from .utils.logger import LoggingBase



class Base(metaclass=LoggingBase):

    CONFIG = None
    ATOMIC_RED_TEAM_REPO = 'https://github.com/redcanaryco/atomic-red-team/zipball/master/'
    command_map = {
        'command_prompt': {
            'windows': 'C:\\Windows\\System32\\cmd.exe',
            'linux': '/bin/sh',
            'macos': '/bin/sh',
            'default': '/bin/sh'
        },
        'powershell': {
            'windows': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
        },
        'sh': {
            'linux': '/bin/sh',
            'macos': '/bin/sh'
        },
        'bash': {
            'linux': '/bin/bash',
            'macos': '/bin/bash'
        }
    }
    _replacement_strings = [
        '#{{{0}}}',
        '${{{0}}}'
    ]

    def download_atomic_red_team_repo(self, save_path, **kwargs) -> str:
        """Downloads the Atomic Red Team repository from github

        Args:
            save_path (str): The path to save the downloaded and extracted ZIP contents

        Returns:
            str: A string of the location the data was saved to.
        """
        response = requests.get(Base.ATOMIC_RED_TEAM_REPO, stream=True, **kwargs)
        z = zipfile.ZipFile(BytesIO(response.content))
        z.extractall(save_path)
        return z.namelist()[0]

    def get_local_system_platform(self) -> str:
        """Identifies the local systems operating system platform

        Returns:
            str: The current/local systems operating system platform
        """
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name

    def get_abs_path(self, value) -> str:
        """Formats and returns the absolute path for a path value

        Args:
            value (str): A path string in many different accepted formats

        Returns:
            str: The absolute path of the provided string
        """
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def show_details(self, value) -> None:
        """Displays the provided value string if Base.CONFIG.show_details is True

        Args:
            value (str): A string to display if selected in config.
        """
        if Base.CONFIG.show_details:
            self.__logger.info(value)

    def prompt_user_for_input(self, title, input_object):
        """Prompts user for input values based on the provided values.
        """
        print(f"""
Inputs for {title}:
    Input Name: {input_object.name}
    Default:     {input_object.default}
    Description: {input_object.description}
""")
        print(f"Please provide a value for {input_object.name} (If blank, default is used):",)
        value = sys.stdin.readline()
        if bool(value):
            return value
        return input_object.default

    def parse_input_lists(self, value):
        value_list = None
        if not isinstance(value, list):
            value_list = set([t.strip() for t in value.split(',')])
        else:
            value_list = set(value)
        return list(value_list)

    def _replace_command_string(self, command: str, path:str, input_arguments: list=[]):
        if command:
            # TODO: Figure out how to handle remote execution of these dependencies (e.g. T1037\\src\\batstartup.bat)
            try:
                command = command.replace('$PathToAtomicsFolder', path)
                command = command.replace('PathToAtomicsFolder', path)
            except:
                pass
            if input_arguments:
                for input in input_arguments:
                    for string in self._replacement_strings:
                        try:
                            command = command.replace(str(string.format(input.name)), str(input.value))
                        except:
                            # catching errors since some inputs are actually integers but defined as strings
                            pass
        return command
