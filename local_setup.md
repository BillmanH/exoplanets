# Getting the game working on your local machine. 

The game is designed to be able to clone the repository and run right away, there are just a couple of steps. 

1. clone the repo from github to your local machine

2. build the anaconda environment
You can run the application on your local machine without cloud resources. I'm using anaconda so you should be able to build the environment in any system with: 
```
conda env create --file=environment.yaml
``` 

and update it using:
```
conda env update --name exoplanets --file=environment.yaml --prune
```

3. you need to set the local environment variables. See the infra section for a list of those variables. 
To access the cosmos DB, you'll need to setup the environment variables. 
```
conda env config vars set endpoint=<copy paste from azure portal>
```
you'll need to add the variables one at a time. I don't have a script for this but the format is simple. 

**NOTE** I created a ps script that syncs between local and cloud. Have a look at `setting_local-env_vars.ps1` in the _infra_ folder. 


Note that some keys are omited in the script and will need to be set manually. After entering keys you can confirm with:
```
conda env config vars list
```
If any variables are missing (you'll find out when you run `python manage.py runserver`) you can add/update them with
```
conda env config vars set varname=value
```

3. Make your migrations

If this is your first time building the application, you will need to update the login data using:
```
python manage.py makemigrations
python manage.py migrate
```