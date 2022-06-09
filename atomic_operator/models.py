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


@define
class BaseFrameworkConfig:
    content_path: DirectoryPath = field()


@define
class EmulationTestsConfig:
    name: AnyStr = field()
    input_arguments: dict = field(factory=dict)
    inventories: List = field(factory=list)


@define
class AdversaryEmulationConfig(BaseFrameworkConfig):
    tests: List[EmulationTestsConfig] = field()

    def __attrs_post_init__(self):
        if self.tests:
            return_list = []
            for item in self.tests:
                return_list.append(EmulationTestsConfig(**item))
            self.tests = return_list


@define
class AtomicTestsConfig:
    guid: AnyStr = field()
    input_arguments: dict = field(factory=dict)
    inventories: List = field(factory=list)


@define
class AtomicConfig(BaseFrameworkConfig):
    tests: List[AtomicTestsConfig]

    def __attrs_post_init__(self):
        if self.tests:
            return_list = []
            for item in self.tests:
                return_list.append(AtomicTestsConfig(**item))
            self.tests = return_list


@define
class ConfigFrameworks:
    adversary_emulations: AdversaryEmulationConfig = field(default=dict)
    atomic_tests: AtomicConfig = field(default=dict)

    def __attrs_post_init__(self):
        if self.adversary_emulations:
            self.adversary_emulations = AdversaryEmulationConfig(**self.adversary_emulations)
        if self.atomic_tests:
            self.atomic_tests = AtomicConfig(**self.atomic_tests)
    
@define
class InventoryConfig:
    name: AnyStr = field()
    hosts: list = field()
    executor: AnyStr = field()


@define
class ConfigFile:
    frameworks: ConfigFrameworks = field()
    inventory: List[InventoryConfig] = field(factory=list)

    def __attrs_post_init__(self):
        if self.frameworks:
            try:
                self.frameworks = ConfigFrameworks(**self.frameworks)
            except TypeError as te:
                raise te
        if self.inventory:
            from .models import Host
            return_list = []
            for item in self.inventory:
                host_list = []
                for host in item.get('hosts'):
                    host_list.append(
                        Host(
                            hostname=host,
                            username=item.get('username'),
                            password=item.get('password'),
                            ssh_key_path=item.get('ssh_key_path'),
                            private_key_string=item.get('private_key_string'),
                            verify_ssl=item.get('verify_ssl', False),
                            ssh_port=item.get('port') or item.get('ssh_port'),
                            ssh_timeout=item.get('timeout') or item.get('ssh_timeout') 
                        )
                    )
                return_list.append(
                    InventoryConfig(
                        name=item['name'],
                        hosts=host_list,
                        executor=item['executor']
                    )
                )
            self.inventory = return_list

