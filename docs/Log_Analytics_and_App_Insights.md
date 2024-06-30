# Live Analytics with App Insights:


```
union traces
| where timestamp > ago(3d)
| where message has "EXOADMIN:"
| where message has "People at this location will starve"
| order by timestamp desc
```

For a specific invocation at that time:
```
union traces
| where timestamp > ago(3d)
| where operation_Id == "3d289db0edabbad600aa68b029d31837"
| where message has "EXOADMIN:"
| order by timestamp desc
```


Graphing:
```
union traces
| where timestamp > ago(3d)
| where message has "EXOADMIN:"
| where message has "organics:"
| order by timestamp desc
```

{'replenish_rate': 10, 'volume': 0, 'name': 'organics', 'objid': '4297972133845', 'max_volume': 1053, 'description': 'bilogical material that can be consumed by pops', 'userguid': 'ac5b8081-7ef9-4bce-baac-6d0ea7e1782c', 'objtype': 'resource', 'id': '4297972133845'} 
