import sys
from typing import (
    AnyStr,
    List
)
from attr import (
    define,
    field,
)
from pydantic import (
    FilePath
)


REPLACEMENT_STRINGS = [
    '#{{{0}}}',
    '${{{0}}}'
]
VARIABLE_REPLACEMENTS = {
    'command_prompt': {
        '%temp%': "$env:TEMP"
    }
}


@define
class ExecutorBase:

    def _prompt_user_for_input(self, title, input_object):
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

    def _replace_command_string(self, command: str, path:str, executor: str, input_arguments: list = [], elevation_required: bool = False):
        if command:
            if elevation_required:
                if executor in ['powershell']:
                    command = f"Start-Process PowerShell -Verb RunAs; {command}"
                elif executor in ['cmd', 'command_prompt']:
                    command = f'cmd.exe /c "{command}"'
                elif executor in ['sh', 'bash', 'ssh']:
                    command = f"sudo {command}"
            command = self._path_replacement(command, path)
            if input_arguments:
                for input in input_arguments:
                    for string in REPLACEMENT_STRINGS:
                        try:
                            command = command.replace(str(string.format(input.name)), str(input.value))
                        except:
                            # catching errors since some inputs are actually integers but defined as strings
                            pass
                    if VARIABLE_REPLACEMENTS.get(executor):
                        for key,val in VARIABLE_REPLACEMENTS[executor].items():
                            try:
                                command = command.replace(key, val)
                            except:
                                pass
            return self._path_replacement(command, path)

    def _set_input_arguments(self, input_arguments):
        if input_arguments:
            from ..base import Base
            for input in input_arguments:
                if Base.CONFIG.kwargs and Base.CONFIG.kwargs.get(input.name):
                    input.value = Base.CONFIG.kwargs[input.name]
                if Base.CONFIG.prompt_for_input_args:
                    input.value = self._prompt_user_for_input(
                        title=self.name,
                        input_object=input
                    )
                if input.value == None:
                    input.value = input.default
        return input_arguments

    def _get_formatted_command(self, command, executor, input_arguments, elevation_required):
        input_arguments = self._set_input_arguments(input_arguments=input_arguments)
        from ..base import Base

        return self._replace_command_string(
            command=command,
            path=Base.CONFIG.content_path,
            executor=executor,
            input_arguments=input_arguments,
            elevation_required=elevation_required
        )


@define
class CapturedOutput:
    out: AnyStr = field(factory=str)
    returncode: AnyStr = field(factory=str)
    errors: AnyStr = field(factory=str)


@define
class Executor(ExecutorBase):
    name: AnyStr = field()
    command: AnyStr = field()
    cleanup_command: AnyStr = field(default=None)
    elevation_required: bool = field(default=False)
    steps: AnyStr = field(default=None)
    captured_output: CapturedOutput = field(factory=CapturedOutput)
    cleanup_output: CapturedOutput = field(factory=CapturedOutput)

    def get_command(self, input_arguments):
        if self.command:
            return self._get_formatted_command(
                command=self.command,
                executor=self.name,
                input_arguments=input_arguments,
                elevation_required=self.elevation_required
            )

    def get_cleanup_command(self, input_arguments):
        if self.cleanup_command:
            return self._get_formatted_command(
                command=self.cleanup_command,
                executor=self.name,
                input_arguments=input_arguments,
                elevation_required=self.elevation_required
            )


@define
class Dependency(ExecutorBase):
    description:        AnyStr = field()
    get_prereq_command: AnyStr = field(default=None)
    prereq_command:     AnyStr = field(default=None)
    get_prereq_command_output: CapturedOutput = field(factory=CapturedOutput)
    prereq_command_output: CapturedOutput = field(factory=CapturedOutput)

    def get_get_prereqs_command(self, executor: str, input_arguments: list = [], elevation_required: bool = False):
        if self.get_prereq_command:
            return self._get_formatted_command(
                command=self.get_prereq_command,
                executor=executor,
                input_arguments=input_arguments,
                elevation_required=elevation_required
            )

    def get_check_prereqs_command(self, executor: str, input_arguments: list = [], elevation_required: bool = False):
        if self.prereq_command:
            return self._get_formatted_command(
                command=self.prereq_command,
                executor=executor,
                input_arguments=input_arguments,
                elevation_required=elevation_required
            )


@define
class InputArguments:
    name:        AnyStr = field()
    description: AnyStr = field()
    type:        AnyStr = field()
    default:     AnyStr or int = field(default=None)
    value:       AnyStr or int = field(default=None)
    source:      AnyStr = field(default=None)
    destination: AnyStr = field(default=None)


@define
class TestBase:
    name: AnyStr = field()
    description: AnyStr = field()


@define
class FrameworkBase:
    path: FilePath = field()
