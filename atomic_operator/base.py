import os
from pathlib import Path, PurePath
import zipfile
from io import BytesIO
import platform

import yaml
import requests
from pick import pick

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    CONFIG = None
    ATOMIC_RED_TEAM_REPO = 'https://github.com/redcanaryco/atomic-red-team/zipball/master/'
    ADVERSARY_EMULATION_LIBRARY_REPO = 'https://github.com/center-for-threat-informed-defense/adversary_emulation_library/zipball/master/'
    COMMAND_MAP = {
        'command_prompt': {
            'windows': 'C:\\Windows\\System32\\cmd.exe',
            'linux': '/bin/sh',
            'macos': '/bin/sh',
            'default': '/bin/sh'
        },
        'cmd': {
            'windows': 'C:\\Windows\\System32\\cmd.exe',
            'linux': '/bin/sh',
            'macos': '/bin/sh',
            'default': '/bin/sh'
        },
        'process': {
            'linux': None
        },
        'powershell': {
            'windows': 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
        },
        'pwsh': {
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
    VARIABLE_REPLACEMENTS = {
        'command_prompt': {
            '%temp%': "$env:TEMP"
        }
    }
    _replacement_strings = [
        '#{{{0}}}',
        '${{{0}}}'
    ]

    def download_github_repo(self, save_path, type, **kwargs) -> str:
        """Downloads the Atomic Red Team repository from github

        Args:
            save_path (str): The path to save the downloaded and extracted ZIP contents

        Returns:
            str: A string of the location the data was saved to.
        """
        if type == 'atomic-red-team':
            url = Base.ATOMIC_RED_TEAM_REPO
        elif type == 'adversary-emulation':
            url = Base.ADVERSARY_EMULATION_LIBRARY_REPO
        else:
            raise ValueError(f"You provided an unknown type value when trying to download a github report: {type}")
        self.__logger.debug(f"Save path is {save_path}")
        response = requests.get(url, stream=True, **kwargs)
        z = zipfile.ZipFile(BytesIO(response.content))
        with zipfile.ZipFile(BytesIO(response.content)) as zf:
            for member in zf.infolist():
                file_path = os.path.realpath(os.path.join(save_path, member.filename))
                if file_path.startswith(os.path.realpath(save_path)):
                    try:
                        zf.extract(member, path=save_path)
                    except FileNotFoundError as fe:
                        self.__logger.critical(f"Unable to find file or folder! {member.filename}")
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

    def _get_file_name(self, path) -> str:
        return path.name.rstrip('.yaml')

    def _find_content(self, path, pattern):
        result = []
        path = PurePath(path)
        for p in Path(path).rglob(pattern):
            result.append(p.resolve())
        return result

    def load_yaml(self, path_to_dir) -> dict:
        """Loads a provided yaml file which is typically an Atomic or Emulation plan defintiion or configuration file.

        Args:
            path_to_dir (str): A string path to a yaml formatted file

        Returns:
            dict: Returns the loaded yaml file in a dictionary format
        """
        if path_to_dir and self.get_abs_path(path_to_dir):
            path = self.get_abs_path(path_to_dir)
            if not os.path.exists(path):
                raise FileNotFoundError("Please make sure the provided file path exists.")
            try:
                with open(self.get_abs_path(path_to_dir), 'r', encoding="utf-8") as f:
                    return yaml.safe_load(f.read())
            except:
                self.__logger.warning(f"Unable to load technique in '{path_to_dir}'")
                
            try:
                # windows does not like get_abs_path so casting to string
                with open(str(path_to_dir), 'r', encoding="utf-8") as f:
                    return yaml.safe_load(f.read())
            except OSError as oe:
                self.__logger.warning(f"Unable to load technique in '{path_to_dir}': {oe}")

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

    def _replace_command_string(self, command: str, path:str, input_arguments: list=[], executor=None):
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
                    if executor and self.VARIABLE_REPLACEMENTS.get(executor):
                        for key,val in self.VARIABLE_REPLACEMENTS[executor].items():
                            try:
                                command = command.replace(key, val)
                            except:
                                pass
        return self._path_replacement(command, path)

    def _check_if_aws(self, test):
        if hasattr(test, 'supported_platforms'):
            if 'iaas:aws' in test.supported_platforms and self.get_local_system_platform() in ['macos', 'linux']:
                return True
        return False

    def _check_platform(self, test, show_output=False) -> bool:
        if self._check_if_aws(test):
            return True
        if hasattr(test, 'supported_platforms'):
            if test.supported_platforms and self.get_local_system_platform() not in test.supported_platforms:
                self.__logger.info(f"You provided a test ({test.auto_generated_guid}) '{test.name}' which is not supported on this platform. Skipping...")
                return False
        elif hasattr(test, 'platforms'):
            if test.platforms and self.get_local_system_platform() not in test.platforms:
                self.__logger.info(f"You provided a test ({test.id}) '{test.name}' which is not supported on this platform. Skipping...")
                return False
        return True

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
