import os
from atomic_operator.atomic.loader import Loader
from atomic_operator.parser import ConfigParser


def test_download_of_atomic_red_team_repo():
    from atomic_operator import AtomicOperator
    AtomicOperator().get_atomics(desintation=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for item in os.listdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
        if 'redcanaryco-atomic-red-team' in item and os.path.isdir(item):
            assert True

def test_loading_of_technique():
    assert Loader().load_technique(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml'))

def test_parsing_of_config():
    data = ConfigParser(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml'))
    assert isinstance(data, ConfigParser)
    assert data.is_defined('f7e6ec05-c19e-4a80-a7e7-241027992fdb')
    inputs = data.get_inputs('f7e6ec05-c19e-4a80-a7e7-241027992fdb')
    assert inputs.get('output_file')
    assert inputs.get('input_file')
    assert data.is_defined('3ff64f0b-3af2-3866-339d-38d9791407c3')
    assert data.is_defined('32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2')
