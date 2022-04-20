import os
from pytest import raises
from atomic_operator.frameworks.loader import Loader
from atomic_operator.frameworks.emulation import EmulationPlanDetails, EmulationPhase



def test_load_emulation_plan():
    path = os.path.join(os.path.dirname(__file__), 'data', 'test_emulation_plan.yml')
    data = Loader().load_yaml(path)
    print(data)

    if isinstance(data, list):
        phase_list = []
        for i in data:
            if not i.get('emulation_plan_details') and i.get('id'):
                phase_list.append(EmulationPhase(**i))
        emulation = [x for x in data if x.get('emulation_plan_details')]
        if emulation:
            emulation = emulation[0]
            emulation = emulation.pop('emulation_plan_details')
        emulation.update({
            'path': path,
            'phases': phase_list
        })
        data = EmulationPlanDetails(**emulation)

    assert data.id == '123700e5-44c8-4894-a409-6484992c8846'
    assert data.adversary_name == 'FIN6'
    assert data.path == path
    assert isinstance(data.phases, list)
    for phase in data.phases:
        assert phase.name
        assert phase.id
        assert phase.description
        assert phase.tactic
        assert phase.technique.attack_id
        assert phase.technique.name
        assert phase.procedure_group
        assert phase.procedure_step
    input_arguments = {
        'adfind_exe': '/tmp/myoutputfile.txt',
        'adfind_url': '/tmp/myscriptpath.sh',
        'adfind_zip_hash': 'mytargetprocess'
    }
    for phase in data.phases:
        if phase.name == 'Enumerate AD person objects':
            for executor in phase.executors:
                assert executor.name == 'command_prompt'
        