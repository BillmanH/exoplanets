class ActionValidator:
    def __init__(self,agent, actions):
        self.agent = agent
        self.actions = [a for a in actions if a["applies_to"]==agent["objtype"]]

    def check_has_attr(self, action):
        if "requires_attr" in self.actions.keys():
            for req in action['requires_attr'].keys():
                if req not in self.agent.keys():
                    return False  # agent doesn't have the reqired propperty
                if action['requires_attr'][req] > 0:
                    if self.agent[req] < action['requires_attr'][req]:
                        return False  # pop doesn't have the sufficient level of propperty
                if action['requires_attr'][req] < 0:
                    if self.agent[req] > action['requires_attr'][req]:
                        return False  # pop has too high level of propperty

        return True

    def validate(self):
        valid_actions = [act for act in self.actions if self.check_has_attr(act)]
        return valid_actions
    