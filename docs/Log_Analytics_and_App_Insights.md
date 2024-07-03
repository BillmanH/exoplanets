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


## Querying Azure Log Analytics
### Exceptions:
```
exceptions
| where timestamp > ago(2d)
| extend dateformated = format_datetime(timestamp, 'yyyy-MM-dd hh')
| summarize Count=count() by dateformated
| order by dateformated asc
```

Getting the most common stack traces
```
exceptions
| where timestamp > ago(2d)
| summarize Count=count() by innermostMessage, operation_Name
| project-reorder Count, operation_Name
| order by Count desc 
| limit 20
```

Function Executions:
```
union traces
| where timestamp > ago(3d)
| summarize Count=count() by operation_Name, timestamp
| order by timestamp desc
| limit 1000
```