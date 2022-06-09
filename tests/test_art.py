import os
from atomic_operator.frameworks.loader import Loader
from atomic_operator.runlist import RunList



def test_download_of_atomic_red_team_repo():
    from atomic_operator import AtomicOperator
    AtomicOperator().art.get_content(destination=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for item in os.listdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))):
        if 'redcanaryco-atomic-red-team' in item and os.path.isdir(item):
            assert True

def test_loading_of_technique():
    assert Loader().load_yaml(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml'))

def test_parsing_of_config():
    run_list = RunList(
        adversary='apt29',
        config_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'atomic_operator_config.yml')
    )
    assert run_list
