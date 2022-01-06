import os
import sys
import zipfile
from io import BytesIO
import platform
import requests
from pick import pick
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
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            for member in zf.infolist():
                file_path = os.path.realpath(os.path.join(save_path, member.filename))
                if file_path.startswith(os.path.realpath(save_path)):
                    zf.extract(member, save_path)
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

    def _path_replacement(self, string, path):
        try:
            string = string.replace('$PathToAtomicsFolder', path)
        except:
            pass
        try:
            string = string.replace('PathToAtomicsFolder', path)
        except:
            pass
        return string

    def _replace_command_string(self, command: str, path:str, input_arguments: list=[]):
        if command:
            command = self._path_replacement(command, path)
            if input_arguments:
                for input in input_arguments:
                    for string in self._replacement_strings:
                        try:
                            command = command.replace(str(string.format(input.name)), str(input.value))
                        except:
                            # catching errors since some inputs are actually integers but defined as strings
                            pass
        return self._path_replacement(command, path)

    def _check_if_aws(self, test):
        if 'iaas:aws' in test.supported_platforms and self.get_local_system_platform() in ['macos', 'linux']:
            return True
        return False

    def _check_platform(self, test, show_output=False) -> bool:
        if self._check_if_aws(test):
            return True
        if test.supported_platforms and self.get_local_system_platform() not in test.supported_platforms:
            self.__logger.info(f"You provided a test ({test.auto_generated_guid}) '{test.name}' which is not supported on this platform. Skipping...")
            return False
        return True

    def _set_input_arguments(self, test, **kwargs):
        if test.input_arguments:
            if kwargs:
                for input in test.input_arguments:
                    for key,val in kwargs.items():
                        if input.name == key:
                            input.value = val
            if Base.CONFIG.prompt_for_input_args:
                for input in test.input_arguments:
                    input.value = self.prompt_user_for_input(test.name, input)
            for input in test.input_arguments:
                if input.value == None:
                    input.value = input.default

    def select_atomic_tests(self, technique):
        options = None
        test_list = []
        for test in technique.atomic_tests:
            test_list.append(test)
        if test_list:
            options = pick(
                test_list, 
                title=f"Select Test(s) for Technique {technique.attack_technique} ({technique.display_name})", 
                multiselect=True, 
                options_map_func=self.format_pick_options
            )
        return [i[0] for i in options] if options else []

    def format_pick_options(self, option):
        return f"{option.name} ({option.auto_generated_guid})"
