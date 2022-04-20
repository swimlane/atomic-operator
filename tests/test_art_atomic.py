import os
from pytest import raises
from atomic_operator.frameworks.loader import Loader
from atomic_operator.frameworks.atomic import Atomic
from atomic_operator.frameworks.atomictest import AtomicTest
from atomic_operator.frameworks.base import Executor


def test_load_atomic():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic.yml')
    data = Loader().load_yaml(path)
    print(data)
    data.update({'path': path})
    assert Atomic(**data)

def test_atomic_structure():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic.yml')
    data = Loader().load_yaml(path)
    data.update({'path': path})
    atomic = Atomic(**data)
    assert atomic.attack_technique == 'T1003.007'
    assert atomic.display_name == 'OS Credential Dumping: Proc Filesystem'
    assert atomic.path == path

def test_atomic_test_structure():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic.yml')
    data = Loader().load_yaml(path)
    data.update({'path': path})
    atomic = Atomic(**data)
    assert isinstance(atomic.atomic_tests, list)
    for test in atomic.atomic_tests:
        assert isinstance(test, AtomicTest)
        assert test.name
        assert test.description
        assert test.supported_platforms
        assert test.auto_generated_guid
        assert isinstance(test.executor, Executor)

def test_atomic_test_replace_command_strings():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_atomic.yml')
    data = Loader().load_yaml(path)
    data.update({'path': path})
    atomic = Atomic(**data)
    input_arguments = {
        'output_file': '/tmp/myoutputfile.txt',
        'script_path': '/tmp/myscriptpath.sh',
        'pid_term': 'mytargetprocess'
    }
    for test in atomic.atomic_tests:
        if test.name == 'Dump individual process memory with sh (Local)':
            assert test.executor.name == 'sh'
            assert test.executor.elevation_required == True
