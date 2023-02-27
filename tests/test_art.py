import os
from atomic_operator.atomic.loader import Loader
from atomic_operator.configparser import ConfigParser


def test_download_of_atomic_red_team_repo():
    from atomic_operator import AtomicOperator
    AtomicOperator().get_atomics(desintation=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for item in os.listdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
        if 'redcanaryco-atomic-red-team' in item and os.path.isdir(item):
            assert True

def test_loading_of_technique():
    assert Loader().load_technique(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml'))

def test_parsing_of_config():
    from atomic_operator.models import Config
    from atomic_operator.base import Base
    from atomic_operator import AtomicOperator

    atomics_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    AtomicOperator().get_atomics(desintation=atomics_path)
    Base.CONFIG = Config(atomics_path=atomics_path)
    config_parser = ConfigParser(config_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml'))

    assert config_parser.is_defined('f7e6ec05-c19e-4a80-a7e7-241027992fdb')
    inputs = config_parser.get_inputs('f7e6ec05-c19e-4a80-a7e7-241027992fdb')
    assert inputs.get('output_file')
    assert inputs.get('input_file')
    assert config_parser.is_defined('3ff64f0b-3af2-3866-339d-38d9791407c3')
    assert config_parser.is_defined('32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2')
