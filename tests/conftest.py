import pytest


@pytest.fixture
def default_art_fixture():
    from atomic_operator import AtomicOperator
    return AtomicOperator()
