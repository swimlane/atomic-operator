from typing import (
    AnyStr,
)
from attr import (
    define,
    field,
)


@define
class Executor:
    name: AnyStr = field()
    command: AnyStr = field()
    cleanup_command: AnyStr = field(default=None)
    elevation_required: bool = field(default=None)
    steps: AnyStr = field(default=None)


@define
class Dependency:
    description:        AnyStr = field()
    get_prereq_command: AnyStr = field(default=None)
    prereq_command:     AnyStr = field(default=None)


@define
class InputArguments:
    name:        AnyStr = field()
    description: AnyStr = field()
    type:        AnyStr = field()
    default:     AnyStr or int = field(default=None)
    value:       AnyStr or int = field(default=None)
    source:      AnyStr = field(default=None)
    destination: AnyStr = field(default=None)


@define
class TestBase:
    name: AnyStr = field()
    description: AnyStr = field()
    executor: Executor = field()
