import os
from pytest import raises
from atomic_operator.atomic.loader import Loader
from atomic_operator.atomic.atomic import Atomic
from atomic_operator.atomic.atomictest import AtomicTest


def test_load_technique():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic2.yml')
    data = Loader().load_technique(path)
    data.update({'path': path })
    assert isinstance(data, dict)
    

def test_convert_to_atomic_object():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic2.yml')
    data = Loader().load_technique(path)
    data.update({'path': path })
    atomic = Atomic(**data)
    assert isinstance(atomic, Atomic)
    assert len(atomic.atomic_tests) >= 1