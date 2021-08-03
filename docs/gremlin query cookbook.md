# Gremlin Queries
This resource uses a gremlin graph. This is a place to bookmark some gremlin queries that I use over and over again. 

Get everything for a system
```
g.V().hasLabel('system').has('username','{username}').in().valueMap()
```

drop an account, and everything asociated with it. As everything stems out from the `account` node,  
```
g.V().has('username','Billmanh').drop()
```
