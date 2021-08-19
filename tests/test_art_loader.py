import os
from pytest import raises
from atomic_operator.atomic_operator import Loader


def test_loader_attribute_error():
    with raises(AttributeError):
        Loader().load_techniques()

def test_load_technique():
    data = Loader().load_technique(os.path.join(os.path.dirname(__file__), 'data', 'test_atomic.yml'))
    assert isinstance(data, dict)

