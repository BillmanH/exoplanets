# Troubleshooting Azure Python Functions (Python)

There are some docs really good docs [here](https://learn.microsoft.com/en-us/azure/azure-functions/recover-python-functions?tabs=vscode%2Cbash&pivots=python-mode-decorators), but they don't get into some of the actual details that translate error message to azure function. 
The first part to understand is the exact place that your app is failing. Depenidng on where it is failing, the way to troubleshoot could be different. 

In this article: 
| Error | TLDR What to do |
|----------|----------|
| Function doesn't deploy in VSC (or in pipeline)    | redeploy    |
| Function does deploy but doesn't show in the portal | Look up the error and fix your code  |
| Function is triggering, but crashing on execution | Look up the error and fix your code |
| Function is completing successfully, but not doing what you want | Deploy some logs to learn more | 
| Long-term function running is off | Log analytics and KUSTO is your friend | 

When functions are eventhub triggers, they can be tough to troubleshoot because they have to be triggered by event streams. The only real way to troubleshoot them is by deploying them into a dev environment in Azure and watching them go. With all of the tools in Visual Stuido Code you can simulate them locally, but IMO it's not worth it. Just get a small sandbox environment where you can troubleshoot them. 




# Error: Function doesn't deploy in VSC
![Alt text](../docs/img/functiodeployfail.png?raw=true "where is my function failing") 

Pretty much the solution is just to run it again. It might work. Here are some things you can check. 
* Turn off your AZ Function VSC tools like `Azurite Table Service`, `Azureite Queue Service`, etc. that can block VSCs API calls. 
* Make sure the AZ Function you want to deploy to in Azure is running. You can try restarting the function.
* Make sure your app is [not throttled by your daily quota](https://stackoverflow.com/questions/75670569/why-azure-function-with-timer-trigger-suddenly-stops-being-triggered/78098313#78098313)

For the most part, you just deploy your function again and again and eventually it will deploy. 

Even if you are deploying via the AZ CLI, or a devopps pipeline you can still get this issue and will solve it the same way. 



# ERROR: Function does deploy but doesn't show in the portal.
This assumes that you got the green checkbox in your deployment `Deploy to App "myApp" Succeeded`. 

![Alt text](../docs/img/functionnottrigger.png?raw=true "where is my function failing") 

Look for this in the application logs:

![Alt text](../docs/img/function0funcloaded.png?raw=true "where is my function failing") 

That means that it loaded the environment and your code, but when it ran the `python function_app.py` it crashed right away before entering the listening state. 

Most likely the service loaded the new code, but that code crashed when booting up the app:
* `"0 functions loaded"` means that the app booted your code, but wasn't able to get any of the functions to work. 
* You have an issue with your code. 
* Missing a library in the `requirements.txt` is the most common. 
* Variables that are declared outside of the wrapped function.
* Calling files that exist locally, but are ignored or pathed to a different location.
* Modules that have system requirements that the cloud machine doesn't have. 
* As above, make sure your app is [not throttled by your daily quota](https://stackoverflow.com/questions/75670569/why-azure-function-with-timer-trigger-suddenly-stops-being-triggered/78098313#78098313)

### How to see the specific error:
Go to the "Diagnose and solve problems">Search>"Functions that are not triggering".

![Alt text](../docs/img/functionsnottriggering.png?raw=true "where is my function failing") 

If you scroll down you will see stack trace of what has happened. It's not the most readable, but it will tell you what had happened. 

![Alt text](../docs/img/functionsstacktrace.png?raw=true "where is my function failing") 

(I've noted the solution to that issue here)(https://github.com/Azure/azure-functions-python-worker/issues/1262#issuecomment-2129619040).


# Function is triggering, but crashing on execution: 
Probably something wrong with your code, but what? 

Click on the specific function that is failing and go to the `Invocations` tab. 

![Alt text](../docs/img/functioninvocation.png?raw=true "where is my function failing") 

You can see, for each individual execution, what has failed. Click on the `Date (UTC)` and it will take you to the logs for that function. 

![Alt text](../docs/img/functioninvocationstack.png?raw=true "where is my function failing") 

It's not pretty, but you can see the now obvious error in your programing. 

# Function is completing successfully, but not doing what you want:
Now you've got to get into some logs. 

![Alt text](../docs/img/functioninvokelogs.png?raw=true "where is my function failing") 

You can see in my function logs above that I've got a lot of information. Each step that the function takes is printed out in the logs. Also, all of my python objects have custom `__repr__` functions that give some information as to the object's state. 

Make liberal use of logger functions such as:
```python
logging.info(f"EXOADMIN: {message['agent']['name']}:{message['agent']['objid']} increased by {message['agent']['replenish_rate']}, {message['agent']['volume']}-> {new_volume}")
```
Note that all of my logs begin with `EXOADMIN`. This makes them easy to see, and benefits when querying in Kusto later on. It separates them from log messages sent by the Azure Function system. 

# Long-term function running is off:
Some times your function only fails once in a while and it's difficult to lock down what's happening when it does. Kusto to the rescue. 

### In app insights:
![Alt text](../docs/img/functionappinsights1.png?raw=true "where is my function failing") 

Get the count of failed executions over time. 
```
exceptions
| where timestamp > ago(2d)
| extend dateformated = format_datetime(timestamp, 'yyyy-MM-dd hh')
| where dateformated <> "OTHER"
| summarize Count=count() by dateformated
| order by dateformated asc
```
Pin that chart to a custom dashboard for your project. Share the dashboard with your stakeholders. 

![Alt text](../docs/img/appInsightsboard.png?raw=true "where is my function failing") 

Getting a list of the functions that are failing over time, with the error message: 
```
exceptions
| where timestamp > ago(7d)
| summarize Count=count() by innermostMessage, operation_Name
| project-reorder Count, operation_Name
| order by Count desc 
| limit 20
```

**Note** that the `| limit 20` will keep your query costs down. 

![Alt text](../docs/img/appinisghtsboard2.png?raw=true "where is my function failing") 


## Additional Logging fun:
This you need to customize for your use case, but if you have been good at using logs you can run queries across your invocations. 

for example:
```
union traces
| where timestamp > ago(3d)
| where message has "EXOADMIN:"
| where message has "People at this location will starve"
| order by timestamp desc
```
I want to know how _famine_ is being executed across multiple function invocations. This helps me understand how the function is working in aggregate. 

![Alt text](../docs/img/appinsights_starving.png?raw=true "where is my function failing") 
