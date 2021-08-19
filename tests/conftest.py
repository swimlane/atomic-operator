import atomic_operator
import pytest


@pytest.fixture
def default_art_fixture():
    from atomic_operator import AtomicOperator
    atomic_op = AtomicOperator()
    atomic_op.get_atomics()
    return atomic_op
