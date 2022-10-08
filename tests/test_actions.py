import yaml 

must_have_attrs = ['type','label','effort','comment','applies_to']


# content of test_sample.py
def load_actions():
    actions_yaml = yaml.safe_load(open(r"..\notebooks\People\actions_pop.yaml"))['actions']
    return actions_yaml

actions = load_actions()

def test_more_than_one_action():    
    assert len(actions)>1  

def action_augments_self_properties(action):
    items = action['augments_self_properties'].split(';')
    properties = items[0].split(',')
    mods = items[1].split(',')
    assert len(properties)==len(mods)

def action_requires_attr(action):
    items = action['requires_attr'].split(';')
    properties = items[0].split(',')
    mods = items[1].split(',')
    assert len(properties)==len(mods)

def action_type_test(action):
    pass


def test_action_properties():
    for action in actions: 
        assert len([atr for atr in must_have_attrs if atr in action.keys()])==len(must_have_attrs)
        assert action['label']=='action'
        if "augments_self_properties" in action.keys():
            action_augments_self_properties(action)
        if "requires_attr" in action.keys():
            action_requires_attr(action)