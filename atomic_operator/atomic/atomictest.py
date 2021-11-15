import typing
import attr


@attr.s
class AtomicTestInput:

    name        = attr.ib()
    description = attr.ib()
    type        = attr.ib()
    default     = attr.ib()
    value       = attr.ib(default=None)
    source      = attr.ib(default=None)
    destination = attr.ib(default=None)


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
    executor                                    = attr.ib()
    input_arguments                             = attr.ib(default=None)
    dependency_executor_name                    = attr.ib(default=None)
    dependencies: typing.List[AtomicDependency] = attr.ib(default=[])

    def __attrs_post_init__(self):
        if self.input_arguments:
            temp_list = []
            for key,val in self.input_arguments.items():
                argument_dict = {}
                argument_dict = val
                argument_dict.update({'name': key, 'value': val.get('default')})
                temp_list.append(AtomicTestInput(**argument_dict))
            self.input_arguments = temp_list
        if self.executor:
            executor_dict = self.executor
            if executor_dict.get('name') == 'manual':
                if not executor_dict.get('command'):
                    executor_dict['command'] = ''
            self.executor = AtomicExecutor(**executor_dict)
            executor_dict = None
        else:
            self.executor = []
        if self.dependencies:
            dependency_list = []
            for dependency in self.dependencies:
                dependency_list.append(AtomicDependency(**dependency))
            self.dependencies = dependency_list
