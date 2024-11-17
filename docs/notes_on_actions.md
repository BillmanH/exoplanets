# Configuration files
* not to be confused with environment vars like connection strings.

Azure functions are deployed separately. For this reason config files related to them are in the `functions` folder. 

for example: `functions\popgrowth\settings.yml`



## Actions and Action Types

actions must have an:
| name | purpose |  
|---|---|
| action  | the thing that is happening |
| agent | the thing that is doing the action or the subject of the action |

and can have: 
| name | purpose |  
|---|---|
| job  | the job which refers to when the action will finish |
| object | the thing that the agent is doing the action to |


### Some Examples of actions:
```yaml
starving_action
    type: starve
    label: action
    applies_to: pop
    effort: 0
    augments_self_properties: {"health": -7}
    comment: Populations that don't have enough resources will loose health until it reachees zero
```

### Some examples of jobs:
```yaml
starving_job
    created_at': 123456
    objid': 123456
    actionType: automatic
```

* action types that are automatic, do not require an agent. They resolve themesleves. 