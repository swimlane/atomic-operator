import os
import atomic_operator

import pytest


@pytest.fixture
def default_art_fixture():
    from atomic_operator import AtomicOperator
    atomic_op = AtomicOperator()
    return atomic_op
