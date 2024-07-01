# Troubleshooting Azure Python Functions

There are some docs really good docs (here)[https://learn.microsoft.com/en-us/azure/azure-functions/recover-python-functions?tabs=vscode%2Cbash&pivots=python-mode-decorators], but they don't get into some of the actual details that translate error message to azure function. 


## Event Hub functions in Python
Most docs are about HTPP functions which are easier to debug. Eventhub trigger functions are tricky because they require an event hub message to trigger them. The way to test them is to create a script that arbitrarily sends test EH messages. There is an example of the (send EH messages in a python script)[https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send?tabs=passwordless%2Croles-azure-portal#send-events]


## Error: Function doesn't deploy in VSC
Pretty much the solution is just to run it again. It might work. Here are some things you can check. 
* Turn off your AZ Function VSC tools like `Azurite Table Service`, `Azureite Queue Service`, etc. that can block VSCs API calls. 
* Make sure the AZ Function you want to deploy to in Azure is running. You can try restarting the function.
* Make sure your app is [not throttled by your daily quota](https://stackoverflow.com/questions/75670569/why-azure-function-with-timer-trigger-suddenly-stops-being-triggered/78098313#78098313)

![Alt text](../docs/img/azurefunction_vsc_deploy.png?raw=true "infra")
For the most part, you just run your function again and again and eventually it will deploy. 

## Function does deploy but doesn't show in the portal.
This assumes that you got the green checkbox in your deployment `Deploy to App "myApp" Succeeded`. Again, there can be many causes. 

A common cause is that the function, on startup, crashed while defining the functions. The most common reason is that you are importing a module that isn't in your requirements.txt file. But it could also be because of a missing `]` or anything that would make the application crash if you were to run it locally.
(I've noted the solution to that issue here)(https://github.com/Azure/azure-functions-python-worker/issues/1262#issuecomment-2129619040).

* If you get the error `Module not found` and you are _sure_ that it's in the requirements.txt. Redeploy your app. That just happens sometimes. 


# Looking at the error messages  
You should make use of the `logging.info` capabilities. You can get those logs in App Insights, are available in the portal as well. 
