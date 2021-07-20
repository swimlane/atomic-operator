from pathlib import PurePath
import typing
import attr

from ..base import Base
from ..config import Config


@attr.s
class AtomicTestInput:

    name = attr.ib()
    description = attr.ib()
    type = attr.ib()
    default = attr.ib()


@attr.s
class AtomicExecutor:

    name                     = attr.ib()
    command                  = attr.ib()
    cleanup_command          = attr.ib(default=None)
    elevation_required       = attr.ib(default=False)
    steps                    = attr.ib(default=None)


@attr.s
class AtomicDependency:

    description = attr.ib()
    get_prereq_command = attr.ib(default=None)
    prereq_command = attr.ib(default=None)


@attr.s
class AtomicTest:
    """A single Atomic test object structure

    Returns:
        AtomicTest: A single Atomic test object
    """

    name                                        = attr.ib()
    description                                 = attr.ib()
    supported_platforms                         = attr.ib()
    auto_generated_guid                         = attr.ib()
    executor: typing.List[AtomicExecutor]       = attr.ib()
    input_arguments                             = attr.ib(default=None)
    dependency_executor_name                    = attr.ib(default=None)
    dependencies: typing.List[AtomicDependency] = attr.ib(default=[])
    # temporary until Atomics are updated - https://github.com/redcanaryco/atomic-red-team/pull/1555
    get_prereq_command = attr.ib(default=None)
    prereq_command = attr.ib(default=None)
    # temporary until Atomics are updated - https://github.com/redcanaryco/atomic-red-team/pull/1555
    _replacement_strings                        = attr.ib(init=False, default=[
        '#{{{0}}}',
        '${{{0}}}'
    ])

    def __attrs_post_init__(self):
        if self.input_arguments:
            temp_list = []
            for key,val in self.input_arguments.items():
                argument_dict = {}
                argument_dict = val
                argument_dict.update({'name': key})
                temp_list.append(AtomicTestInput(**argument_dict))
            self.input_arguments = temp_list
        # temporary until fixed by Atomics - https://github.com/redcanaryco/atomic-red-team/pull/1554
        temp_prereq_command = None
        if self.executor:
            executor  = []
            if self.executor.get('name') == 'manual':
                if not self.executor.get('command'):
                    self.executor['command'] = ''
            # Temporary until Atomics are fixed
            if self.executor.get('cleanup') and not self.executor.get('cleanup_command'):
                self.executor['cleanup_command'] = self.executor['cleanup']
                self.executor.pop('cleanup')

            # Temporary until Atomics are fixed - https://github.com/redcanaryco/atomic-red-team/pull/1554
            if self.executor.get('prereq_command'):
                temp_prereq_command = self.executor['prereq_command']
                self.executor.pop('prereq_command')
            executor.append(AtomicExecutor(**self.executor))
            self.executor = executor
        if self.dependencies:
            dependency_list = []
            for dependency in self.dependencies:
                dependency_list.append(AtomicDependency(**dependency))
            self.dependencies = dependency_list
        elif not self.dependencies and temp_prereq_command:
            dependency_list = []
            dependency_list.append(AtomicDependency(
                description='',
                prereq_command=temp_prereq_command
            ))
            self.dependencies = dependency_list

    def __replace_command_string(self, command: str):
        if command:
            # TODO: Figure out how to handle remote execution of these dependencies (e.g. T1037\\src\\batstartup.bat)
            command = command.replace('$PathToAtomicsFolder', str(PurePath(Base.CONFIG.atomics_path)))
            command = command.replace('PathToAtomicsFolder', str(Base.CONFIG.atomics_path))
            if self.input_arguments:
                for input in self.input_arguments:
                    for string in self._replacement_strings:
                        command = command.replace(str(string.format(input.name)), str(input.value))
        return command

    def set_command_inputs(self, **kwargs):
        # Only parse for inputs defined. If not defined then ignore kwargs
        if self.input_arguments:
            for arguments in self.input_arguments:
                if kwargs and kwargs.get(arguments.name):
                    arguments.value = kwargs[arguments.name]
                else:
                    arguments.value = arguments.default
        if self.executor:
            for executor in self.executor:
                executor.command = self.__replace_command_string(executor.command)
                executor.cleanup_command = self.__replace_command_string(executor.command)
        if self.dependencies:
            for dependency in self.dependencies:
                dependency.description = self.__replace_command_string(dependency.description)
                dependency.get_prereq_command = self.__replace_command_string(dependency.get_prereq_command)
                dependency.prereq_command = self.__replace_command_string(dependency.prereq_command)
