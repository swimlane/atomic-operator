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
    TestBase,
    Executor,
    Dependency,
    InputArguments
)
from .semversion import SemVersion
from ..models import Host


@define
class Technique:
    attack_id: AnyStr = field()
    name: AnyStr = field()


@define
class Command:
    command: AnyStr = field()
    payloads: List = field()


@define
class CommandPrompt:
    cmd: Command = field()


@define
class WindowsPlatform:
    windows: CommandPrompt = field()


@define
class EmulationPhase(TestBase):
    id: AnyStr = field()
    tactic: AnyStr = field()
    technique: Technique = field()
    procedure_group: AnyStr = field()
    procedure_step: SemVersion = field()
    platforms: WindowsPlatform = field()
    cti_source: HttpUrl = field(default=None)
    input_arguments                             = field(default=None)
    dependency_executor_name                    = field(default=None)
    dependencies: List[Dependency] = field(default=[])
    executors: List[Executor] = field(default=[])

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


@define
class EmulationPlanDetails:
    id: AnyStr = field()
    adversary_name: AnyStr = field()
    adversary_description: AnyStr = field()
    attack_version: int = field()
    format_version: int = field()
    path: AnyStr = field()
    phases: List[EmulationPhase] = field()
    hosts: List[Host] = field(default=[])
