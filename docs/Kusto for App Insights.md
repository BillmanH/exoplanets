
# Kusto in Application insights

Application insights for my stack traces. 
```kusto
traces
| where timestamp > ago(7d)
| order by timestamp desc
| where message has "EXOADMIN:"
| limit 100
```
My logs in AZ functions all have `EXOADMIN:` tagged so it is easy to filter out the az log stuff. 


You can also filter by the type of action
```kusto
traces
| where timestamp > ago(7d)
| order by timestamp desc
| where message has "EXOADMIN:"
| where message has "CONSUMPTION"
| limit 100
```
the types are: `CONSUMPTION`, `REPRODUCTION`, `CONSUMPTION`, `RENEWAL` as of right now. You can see the full list in the code under `function_app.py`.
Note that if you are hunting for a specific `operation_id` then you can use the tag: `-------And with that processed a JOB:`.

Tracing Jobs:
```kusto
traces
| where timestamp > ago(7d)
| order by timestamp desc
| where message has "EXOADMIN: messages:"
| where message !has "job:0"
| limit 100
```

## Tracking the data for a specific job. 
first you need to get the `operation_Id` of your function run. You get this from the queries above. 

```
traces
| where timestamp > ago(30d)
| where operation_Id == <Your operation_Id>
| order by timestamp asc
```


## Some more advanced examples
Get all of the counts of functions jobs
```
traces
| where timestamp > ago(7d)
| order by timestamp desc
| where message has "EXOADMIN: messages:"
| limit 100
```

