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
    cti_source: HttpUrl = field()
    procedure_group: AnyStr = field(validator=validators.in_['procedure_discovery', 'procedure_privesc', 'procedure_cred_access', 'procedure_collection', 'procedure_exfiltration', 'procedure_pos_execution', 'procedure_pos_persistence', 'procedure_pos_exfiltration', 'procedure_ransomware_distribution', 'procedure_lateral_movement', 'procedure_ransomware_copy', 'procedure_ransomware_distribute', 'procedure_ransomware_execute_wmic', 'procedure_ransomware_execute_psexec', 'procedure_ransomware_psexec'])
    procedure_step: SemVersion = field()
    platforms: WindowsPlatform = field()
    input_arguments                             = field(default=None)
    dependency_executor_name                    = field(default=None)
    dependencies: List[Dependency] = field(default=[])

    def __attrs_post_init__(self):
        if self.input_arguments:
            temp_list = []
            for key,val in self.input_arguments.items():
                argument_dict = {}
                argument_dict = val
                argument_dict.update({'name': key, 'value': val.get('default')})
                temp_list.append(InputArguments(**argument_dict))
            self.input_arguments = temp_list
        if self.executor:
            executor_dict = self.executor
            if executor_dict.get('name') == 'manual':
                if not executor_dict.get('command'):
                    executor_dict['command'] = ''
            self.executor = Executor(**executor_dict)
            executor_dict = None
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
