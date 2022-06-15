from typing import AnyStr, List

from attr import define, field

from .base import (
    TestBase,
    Executor,
    Dependency,
    InputArguments
)


@define
class AtomicTest(TestBase):
    """A single Atomic test object structure.

    Returns:
        AtomicTest: A single Atomic test object
    """
    supported_platforms:      AnyStr               = field()
    auto_generated_guid:      AnyStr               = field()
    executor:                 Executor             = field()
    input_arguments:          List[InputArguments] = field(factory=list)
    dependency_executor_name: AnyStr               = field(factory=str)
    dependencies:             List[Dependency]     = field(factory=list)

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

    def get_command(self):
        self._set_input_arguments()
        if self.executor.command:
            from ..base import Base
            return self._replace_command_string(
                command=self.executor.command,
                path=Base.CONFIG.atomics_path,
                executor=self.executor.name,
                input_arguments=self.input_arguments,
                elevation_required=self.executor.elevation_required
            )

    def get_cleanup_command(self):
        self._set_input_arguments()
        if self.executor.cleanup_command:
            from ..base import Base
            return self._replace_command_string(
                command=self.executor.cleanup_command,
                path=Base.CONFIG.atomics_path,
                executor=self.executor.name,
                input_arguments=self.input_arguments,
                elevation_required=self.executor.elevation_required
            )
