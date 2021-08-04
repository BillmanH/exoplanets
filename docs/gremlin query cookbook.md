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

Drop an account, and everything asociated with it. Everything for a user has the 'username' property.   
```
g.V().has('username','Billmanh').drop()
```
