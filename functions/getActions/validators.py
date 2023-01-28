import logging
class ActionValidator:
    def __init__(self,agent, actions):
        self.agent = agent
        self.actions = [a for a in actions if a["applies_to"]==agent["objtype"]]
        

    def check_has_attr(self, action):
        if "requires_attr" in action.keys():
            for req in action['requires_attr'].keys():
                if req not in self.agent.keys():
                    logging.info(f'agent doesn\'t have the reqired propperty {req}: {action["type"]}')
                    return False  
                if action['requires_attr'][req] > 0:
                    if self.agent[req] < action['requires_attr'][req]:
                        logging.info(f'agent doesn\'t have the sufficient level of propperty {req}: {action["type"]}')
                        return False 
                if action['requires_attr'][req] < 0:
                    if self.agent[req] > action['requires_attr'][req]:
                        logging.info(f'agent has too high level of propperty {req}: {action["type"]}')
                        return False 

        return True

    def validate(self):
        logging.info(f'agent has: {len(self.actions)} actions')
        valid_actions = [act for act in self.actions if self.check_has_attr(act)]
        return valid_actions
    