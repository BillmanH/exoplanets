# swithc to the env that has the local variables
conda activate exoplanets

# start the interactive login
az login
az account set --subscription $Env:subscription
cd $Env:abspath



# az group delete -g exodestiny