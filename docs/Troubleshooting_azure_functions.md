# Troubleshooting Azure Python Functions (Python)

There are some docs really good docs (here)[https://learn.microsoft.com/en-us/azure/azure-functions/recover-python-functions?tabs=vscode%2Cbash&pivots=python-mode-decorators], but they don't get into some of the actual details that translate error message to azure function. 
The first part to understand is the exact place that your app is failing. Depenidng on where it is failing, the way to troubleshoot could be different. 

In this article: 
| Error | TLDR What to do |
|----------|----------|
| Function doesn't deploy in VSC    | redeploy    |
| Function does deploy but doesn't show in the portal | Look up the error and fix your code  |
| Function is triggering, but crashing on execution | Look up the error and fix your code |

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


# The app is triggering, but crashing on execution. 
Probably something wrong with your code, but what? 

Click on the specific function that is failing and go to the `Invocations` tab. 

![Alt text](../docs/img/functioninvocation.png?raw=true "where is my function failing") 

You can see, for each individual execution, what has failed. Click on the `Date (UTC)` and it will take you to the logs for that function. 

![Alt text](../docs/img/functioninvocationstack.png?raw=true "where is my function failing") 

It's not pretty, but you can see the now obvious error in your programing. 
