import os
import attr
from .base import Base
from .utils.exceptions import AtomicsFolderNotFound


# Setting frozen to True means immutability (static) values once set
@attr.s(frozen=True)
class Config:

    """The main configuration class used across atomic-operator

    Raises:
        AtomicsFolderNotFound: Raised when unable to find the provided atomics_path value
    """

    atomics_path          = attr.ib()
    check_prereqs         = attr.ib(default=False)
    get_prereqs           = attr.ib(default=False)
    cleanup               = attr.ib(default=False)
    command_timeout       = attr.ib(default=20)
    show_details          = attr.ib(default=False)
    prompt_for_input_args = attr.ib(default=False)
    kwargs                = attr.ib(default={})
    copy_source_files     = attr.ib(default=True)

    def __attrs_post_init__(self):
        object.__setattr__(self, 'atomics_path', self.__get_abs_path(self.atomics_path))

    def __get_abs_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    @atomics_path.validator
    def validate_atomics_path(self, attribute, value):
        value = self.__get_abs_path(value)
        if not os.path.exists(value):
            raise AtomicsFolderNotFound('Please provide a value for atomics_path that exists')


@attr.s
class Host:

    hostname           = attr.ib(type=str)
    username           = attr.ib(default=None, type=str)
    password           = attr.ib(default=None, type=str)
    verify_ssl         = attr.ib(default=False, type=bool)
    ssh_key_path       = attr.ib(default=None, type=str)
    private_key_string = attr.ib(default=None, type=str)
    port               = attr.ib(default=22, type=int)
    timeout            = attr.ib(default=5, type=int)

    @ssh_key_path.validator
    def validate_ssh_key_path(self, attribute, value):
        if value:
            Base.get_abs_path(value)
