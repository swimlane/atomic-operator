import os
from atomic_operator.atomic.loader import Loader
from atomic_operator.base import Base


def test_parsing_of_config():
    data = Base().format_config_data(Loader().load_technique(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml')))
    assert isinstance(data, dict)
    assert data['f7e6ec05-c19e-4a80-a7e7-241027992fdb']
    inputs = ['output_file', 'input_file']
    for key,val in data['f7e6ec05-c19e-4a80-a7e7-241027992fdb'].items():
        assert key in inputs and val is not None
    assert data['3ff64f0b-3af2-3866-339d-38d9791407c3']
    assert '32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2' in data
    assert not data['32f90516-4bc9-43bd-b18d-2cbe0b7ca9b2']