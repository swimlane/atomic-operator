from typing import AnyStr, List

from attr import define, field

from .atomictest import AtomicTest
from .base import FrameworkBase
from ..models import Host


@define
class Atomic(FrameworkBase):
    """A single Atomic data structure. 
    
    Each Atomic (technique) will contain a list of one or more AtomicTest objects.
    """

    attack_technique: AnyStr = field()
    display_name: AnyStr = field()
    atomic_tests: List[AtomicTest] = field()
    hosts: List[Host] = field(factory=list)

    def __attrs_post_init__(self):
        if self.atomic_tests:
            test_list = []
            for test in self.atomic_tests:
                test_list.append(AtomicTest(**test))
            self.atomic_tests = test_list
