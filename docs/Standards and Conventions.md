# Standards used in this application

## Formatting: 
### Dates and Times
```
datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
```
creates the date: `26-12-2021-13-12-03`


## Nodes and Edges
A node **MUST** contain these formats. 
```
user = {
    "label": "obj",
    "objid":  maths.uuid(n=13),
    "name": "name"
}
```
Other items are created when uploading to the graph. Note the `models.create_vertex` function. You don't need to add these things (and shouldn't).
* convert and rounds a number to 4 decimal places, if possible. 
* adds property `username`
* adds property `objtype`, which is just the lable. 
 
Edges, when created in python have this shape:
```
 {"node1": p["objid"], "node2": homeworld["objid"], "label": "enhabits", "weight":.45}
```
 note that the edge automatically links two objects by `objid`. 