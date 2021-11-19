from atomic_operator.configparser import ConfigParser
from atomic_operator.base import Base

def test_config_parser():
    config = ConfigParser(
        config_file='config.example.yml',
        techniques=Base().parse_input_lists("T1003,T1004"),
        host_list=Base().parse_input_lists("123.123.123.123, 1.1.1.1"),
        username='username',
        password='password'
    )
    assert isinstance(config.run_list, list)
