# Gremlin Queries
This resource uses a gremlin graph. This is a place to bookmark some gremlin queries that I use over and over again. 

```
g.V().hasLabel('system').has('username','{username}').in().valueMap()
```
