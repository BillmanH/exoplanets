# Gremlin Queries
This resource uses a gremlin graph. This is a place to bookmark some gremlin queries that I use over and over again. 

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
### Population Queries
Get the average agression for a faction
```
g.V().has('faction','name','factionName').in('isInFaction').values('aggression').mean()
```

## NUCLEAR delete and drop functions, use with caution.
Drop an account, and everything asociated with it. Everything for a user has the 'username' property.  
```
g.V().has('username','Billmanh').drop()
```
