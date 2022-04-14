from typing import (
    AnyStr,
    List
)
from attr import (
    define,
    field
)
from .base import (
    TestBase,
    Executor,
    Dependency,
    InputArguments
)


@define
class AtomicTest(TestBase):
    """A single Atomic test object structure

    Returns:
        AtomicTest: A single Atomic test object
    """
    supported_platforms:      AnyStr = field()
    auto_generated_guid:      AnyStr = field()
    input_arguments                  = field(default=None)
    dependency_executor_name: AnyStr = field(default=None)
    dependencies:             List[Dependency] = field(default=[])

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
