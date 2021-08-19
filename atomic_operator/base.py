import os
import sys
import zipfile
from io import BytesIO
import platform
import subprocess
import requests
from .config import Config
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

    def download_atomic_red_team_repo(self, save_path, **kwargs):
        response = requests.get(Base.ATOMIC_RED_TEAM_REPO, stream=True, **kwargs)
        z = zipfile.ZipFile(BytesIO(response.content))
        z.extractall(save_path)
        return z.namelist()[0]

    def format_config_data(self, config_file):
        return_dict = {}
        if config_file:
            if not os.path.exists(config_file):
                raise Exception('Please provide a config_file path that exists')
            from .atomic.loader import Loader
            config_file = Loader().load_technique(config_file)
            
            if not config_file.get('atomic_tests') and not isinstance(config_file, list):
                raise Exception('Please provide one or more atomic_tests within your config_file')
            for item in config_file['atomic_tests']:
                if item.get('guid') not in return_dict:
                    return_dict[item['guid']] = {}
                if item.get('input_arguments'):
                    for key,val in item['input_arguments'].items():
                        return_dict[item['guid']].update({
                            key: val.get('value')
                        })
        return return_dict

    def get_local_system_platform(self):
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name

    def get_abs_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    def show_details(self, value):
        if Base.CONFIG.show_details:
            self.__logger.info(value)

    def prompt_user_for_input(self, title, input_object):
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

    def print_progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

    def execute_subprocess(self, executor, command, cwd):
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
                timeout=Base.CONFIG.command_timeout
            )
            if p.returncode != 0:
                self.__logger.warning(f"Command: {command} returned exit code {p.returncode}: {outs}")
            return outs, errs
        except subprocess.TimeoutExpired as e:
            # Display output if it exists.
            if e.output:
                print(e.output)
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
            print("Command timed out!")

            # Kill the process.
            p.kill()
            return "", ""