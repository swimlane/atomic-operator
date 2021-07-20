import os
import sys
import platform
import subprocess
from .config import Config
from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

    CONFIG = None
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
        p = subprocess.Popen(executor, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, env=os.environ, cwd=cwd)
        try:

            outs, errs = p.communicate(bytes(command, "utf-8") + b"\n", timeout=Config.command_timeout)
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