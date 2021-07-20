import pytest


@pytest.fixture
def default_art_fixture():
    from atomic_operator import AtomicOperator
    return AtomicOperator()

@pytest.fixture
def art_fixture_with_relative_path():
    from atomic_operator import AtomicOperator
    return AtomicOperator(atomics_path='~')
