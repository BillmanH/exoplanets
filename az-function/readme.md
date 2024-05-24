# Troubleshooting AZ Functions is a Pain

The portal only shows the files in the root directory. 

![Alt text](/docs/img/azfunc_portal_files.png?raw=true "az portal viles view")

The other files are probably there. 

## Are the functions running at all. 
This is difficult to tell as there isn't a way to monitor events. 


### Tracking the time. 
You can confirm that the function is running, because the time is updating. You can track this on the main page. 
14008

Troubleshooting in the loggs:

![alt text](/docs/img/application_insights.png?raw=true "app insights")

# Kusto in Application insights
```kusto
traces
| where customDimensions.LogLevel == "Information"
| order by timestamp desc
| limit 50
```
.

If one of the errors shows `0 functions loaded`, this could mean that a syntax error in your code prevented the function from loading. 
