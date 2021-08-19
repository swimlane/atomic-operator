import os
import atomic_operator

import pytest


@pytest.fixture
def default_art_fixture():
    from atomic_operator import AtomicOperator
    atomic_op = AtomicOperator()
    atomic_op.get_atomics(desintation=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return atomic_op
