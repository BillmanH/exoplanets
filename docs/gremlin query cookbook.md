# Gremlin Queries
This resource uses a gremlin graph. This is a place to bookmark some gremlin queries that I use over and over again. 

## Time
There is only one central time object.
```
g.V().hasLabel('time').valuemap()
```

## Celestial bodies
Get everything for a system
```
g.V().hasLabel('system').has('username','{username}').in().valueMap()
```

Get the soler stystem, aka all the things that orbit something in a system 
```
g.V().hasLabel('system').has('username','userbill').in().inE('orbits')
```

Get the objects orbiting an object.
```
g.V().has('objid','8308379553174').in('orbits').valueMap()
```
## Population Queries
Get the average agression for a faction (average of pop['agression'])
```
g.V().has('faction','name','factionName').in('isInFaction').values('aggression').mean()
```

##  Desires
### Get all of the desired objectives of a pop
```
g.V().has('objid','5720114744401').outE('desires').inV().hasLabel('objective')
```
Getting all of the desires, weights and objectives for a pop
```
g.V().has('objid','4253777177342').outE('desires').inV().dedup().path().by(values('name','objid').fold()).by('weight').by(values('type','objid','comment','leadingAttribute').fold())
```

# Actions
### Getting all unresolved actions

Getting all pending actions, regardless of agent:
```
    g.E().haslabel('takingAction').has('status','pending').as('job')
        .outV().as('agent').path().by(valueMap())
```

## **NUCLEAR** delete and drop functions, use with caution.
Drop an account, and everything asociated with it. Everything for a user has the 'username' property.  
```
g.V().has('username','Billmanh').drop()
```
