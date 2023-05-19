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
g.V().has('faction','name','factionName').in('isIn').values('aggression').mean()
```

get the peopl of a given local, including thier faction and species:
```
g.V().has('objid','7615388501660').as('location')
	.in('inhabits').as('population')
	.local(
		union(
			out('isInFaction').as('faction'),
			out('isOfSpecies').as('species')
			)
			.fold()).as('faction','species')
			.path()
			.by(unfold().valueMap().fold())
```

get all populations that have enough health, where they live and the species
```
g.V().has('label','pop')
    .has('health',gt(0.2)).as('pop')
    .local(
        union(
            out('inhabits').as('location'),
            out('isOfSpecies').as('species')
            )
		    .fold()).as('location','species')
	    .path()
		.by(unfold().valueMap().fold())
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

Getting the pop, planet and action being taken.

```
g.E().haslabel('takingAction')
	.has('status',within('pending','resolved')).as('job')
        .outV().as('agent')
	.out('inhabits').as('location')
	.path().by(values('name','status','weight','comment').fold())
		.by(values('name').fold())
		.by(values('name','class','objtype').fold())
```


## **NUCLEAR** delete and drop functions, use with caution.
Drop an account, and everything asociated with it. Everything for a user has the 'username' property.  
```
g.V().has('username','Billmanh').drop()
```
