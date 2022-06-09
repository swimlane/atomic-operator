import os
from typing import (
    List,
    AnyStr
)
from pydantic import DirectoryPath
from attr import (
    define,
    field
)

from .base import Base
from .utils.exceptions import ContentFolderNotFound


@define
class Host:
    hostname: AnyStr = field(default=None)
    username: AnyStr = field(default=None)
    password: AnyStr = field(default=None)
    ssh_key_path: AnyStr = field(default=None)
    private_key_string: AnyStr = field(default=None)
    verify_ssl: bool = field(default=False)
    ssh_port: int = field(default=None)
    ssh_timeout: int = field(default=None)

    @ssh_key_path.validator
    def validate_ssh_key_path(self, attribute, value):
        if value:
            Base.get_abs_path(value)


# Setting frozen to True means immutability (static) values once set
@define(frozen=True)
class Config:

    """The main configuration class used across atomic-operator

    Raises:
        ContentFolderNotFound: Raised when unable to find the provided content_path value
    """

    content_path: AnyStr        = field()
    check_prereqs: bool         = field(default=False)
    get_prereqs: bool           = field(default=False)
    cleanup: bool               = field(default=False)
    command_timeout: int        = field(default=20)
    debug: bool                 = field(default=False)
    prompt_for_input_args: bool = field(default=False)
    kwargs: dict                = field(default={})
    copy_source_files: bool     = field(default=True)

    def __attrs_post_init__(self):
        object.__setattr__(self, 'content_path', self.__get_abs_path(self.content_path))

    def __get_abs_path(self, value):
        return os.path.abspath(os.path.expanduser(os.path.expandvars(value)))

    @content_path.validator
    def validate_atomics_path(self, attribute, value):
        value = self.__get_abs_path(value)
        if not os.path.exists(value):
            raise ContentFolderNotFound('Please provide a value for content_path that exists')
