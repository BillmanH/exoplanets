# Troubleshooting Azure Python Functions

There are some docs really good docs (here)[https://learn.microsoft.com/en-us/azure/azure-functions/recover-python-functions?tabs=vscode%2Cbash&pivots=python-mode-decorators], but they don't get into some of the actual details that translate error message to azure function. 
The first part to understand is the exact place that your app is failing. Depenidng on where it is failing, the way to troubleshoot could be different. 
![Alt text](../docs/img/functionerrors.png?raw=true "where is my function failing") 

When functions are eventhub triggers, they can be tough to troubleshoot because they have to be triggered by event streams. The only real way to troubleshoot them is by deploying them into a dev environment in Azure and watching them go. With all of the tools in Visual Stuido Code you can simulate them locally, but IMO it's not worth it. Just get a small sandbox environment where you can troubleshoot them. 




## Error: Function doesn't deploy in VSC
![Alt text](../docs/img/functiodeployfail.png?raw=true "where is my function failing") 

Pretty much the solution is just to run it again. It might work. Here are some things you can check. 
* Turn off your AZ Function VSC tools like `Azurite Table Service`, `Azureite Queue Service`, etc. that can block VSCs API calls. 
* Make sure the AZ Function you want to deploy to in Azure is running. You can try restarting the function.
* Make sure your app is [not throttled by your daily quota](https://stackoverflow.com/questions/75670569/why-azure-function-with-timer-trigger-suddenly-stops-being-triggered/78098313#78098313)

![Alt text](../docs/img/azurefunction_vsc_deploy.png?raw=true "infra")
For the most part, you just run your function again and again and eventually it will deploy. 

## ERROR: Function does deploy but doesn't show in the portal.
This assumes that you got the green checkbox in your deployment `Deploy to App "myApp" Succeeded`. Again, there can be many causes. 

A common cause is that the function, on startup, crashed while defining the functions. The most common reason is that you are importing a module that isn't in your requirements.txt file. But it could also be because of a missing `]` or anything that would make the application crash if you were to run it locally.
(I've noted the solution to that issue here)(https://github.com/Azure/azure-functions-python-worker/issues/1262#issuecomment-2129619040).

* If you get the error `Module not found` and you are _sure_ that it's in the requirements.txt. Redeploy your app. That just happens sometimes. 


# Looking at the error messages  
You should make use of the `logging.info` capabilities. You can get those logs in App Insights, are available in the portal as well. 
