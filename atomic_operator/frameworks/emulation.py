from typing import (
    AnyStr,
    List
)
from attr import (
    define,
    field,
    validators
)
from pydantic import (
    HttpUrl
)

from .base import (
    CapturedOutput,
    TestBase,
    Executor,
    ExecutorBase,
    Dependency,
    InputArguments,
    FrameworkBase
)
from .semversion import SemVersion
from ..models import Host


@define
class Technique:
    attack_id: AnyStr = field()
    name: AnyStr = field()


@define
class Command(ExecutorBase):
    command:        AnyStr         = field()
    payloads:       List           = field(factory=list)
    cleanup:        AnyStr         = field(factory=str)
    command_output: CapturedOutput = field(factory=CapturedOutput)
    cleanup_output: CapturedOutput = field(factory=CapturedOutput)

    def get_command(self, executor_name, input_arguments, elevation_required=False):
        if self.command:
            return self._get_formatted_command(
                command=self.command,
                executor=executor_name,
                input_arguments=input_arguments,
                elevation_required=elevation_required
            )

    def get_cleanup_command(self, executor_name, input_arguments, elevation_required=False):
        if self.cleanup:
            return self._get_formatted_command(
                command=self.cleanup,
                executor=executor_name,
                input_arguments=input_arguments,
                elevation_required=elevation_required
            )


@define
class CommandPrompt:
    cmd: Command = field()

    def __attrs_post_init__(self):
        if self.cmd:
            try:
                self.cmd = Command(**self.cmd)
            except Exception as e:
                raise e


@define
class PowerShell:
    pwsh: Command = field()

    def __attrs_post_init__(self):
        if self.pwsh:
            self.pwsh = Command(**self.pwsh)

@define
class Process:
    proc: Command = field()

    def __attrs_post_init__(self):
        if self.proc:
            self.proc = Command(**self.proc)


@define
class Shell:
    sh: Command = field()

    def __attrs_post_init__(self):
        if self.sh:
            self.sh = Command(**self.sh)


@define
class LinuxPlatform:
    linux: Shell or Process = field()
    _executor: AnyStr = field(factory=str)

    def __attrs_post_init__(self):
        if self.linux:
            if self.linux.get('sh'):
                self.linux = Shell(**self.linux)
                self._executor = "sh"
            elif self.linux.get('proc'):
                self.linux = Process(**self.linux)
                self._executor = "process"


@define
class WindowsPlatform:
    windows: CommandPrompt = field()
    _executor: AnyStr = field(factory=str)

    def __attrs_post_init__(self):
        if self.windows:
            if self.windows.get('psh,pwsh'):
                new_windows = {
                    "pwsh": self.windows['psh,pwsh']
                }
                self.windows = PowerShell(**new_windows)
                self._executor = "pwsh"
            elif self.windows.get('cmd'):
                self.windows = CommandPrompt(**self.windows)
                self._executor = "cmd"


@define
class EmulationPhase(TestBase):
    id: AnyStr = field()
    tactic: AnyStr = field()
    technique: Technique = field()
    procedure_group: AnyStr = field()
    procedure_step: SemVersion = field()
    platforms: WindowsPlatform or LinuxPlatform = field()
    cti_source: HttpUrl = field(default=None)
    input_arguments                             = field(default=None)
    dependency_executor_name                    = field(default=None)
    dependencies: List[Dependency] = field(default=[])
    executors: List[Executor] = field(default=[])
    _platform: AnyStr = field(factory=str)

    def __attrs_post_init__(self):
        if self.technique:
            self.technique = Technique(**self.technique)
        if self.input_arguments:
            temp_list = []
            for key,val in self.input_arguments.items():
                argument_dict = {}
                argument_dict = val
                argument_dict.update({'name': key, 'value': val.get('default')})
                temp_list.append(InputArguments(**argument_dict))
            self.input_arguments = temp_list
        if self.executors:
            executor_list = []
            for executor in self.executors:
                if executor.get('name') == 'manual':
                    if not executor.get('command'):
                        executor['command'] = ''
                executor_list.append(Executor(**executor))
            self.executors = executor_list
        else:
            self.executor = []
        if self.dependencies:
            dependency_list = []
            for dependency in self.dependencies:
                dependency_list.append(Dependency(**dependency))
            self.dependencies = dependency_list
        if self.platforms:
            if self.platforms.get('windows'):
                self.platforms = WindowsPlatform(**self.platforms)
                self._platform = "windows"
            elif self.platforms.get('linux'):
                self.platforms = LinuxPlatform(**self.platforms)
                self._platform = "linux"


@define
class EmulationPlanDetails(FrameworkBase):
    id: AnyStr = field()
    adversary_name: AnyStr = field()
    adversary_description: AnyStr = field()
    attack_version: int = field()
    format_version: int = field()
    phases: List[EmulationPhase] = field()
    hosts: List[Host] = field(default=[])
