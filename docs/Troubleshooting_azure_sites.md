

# Azure upgrade erased environment variables. 

1. Look in the loggs in the portal. Go to `Diagnose and solve problems` > `Application logs`

* ModuleNotFoundError: No module named 'django'


| Issue         | Solution     | 
|--------------|-----------|
| `ModuleNotFoundError: No module named 'django'` | The build crashed when building the python environment. Redeploy. |
| `os.environ KeyError` | Redeploying the application has reset the keys. Set keys. instructions in `infra\setting-azure-env_vars.md` |