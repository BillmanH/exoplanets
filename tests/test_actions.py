import yaml 

# content of test_sample.py
def load_actions():
    actions_yaml = yaml.safe_load(open(r"..\notebooks\People\actions_pop.yaml"))['actions']
    return actions_yaml

actions = load_actions()

def test_more_than_one_action():    
    assert len(actions)>1  

def action_augments_self_properties:
    if action['augments_self_properties']:
        
def test_action_properties():
    for action in actions: 
        assert