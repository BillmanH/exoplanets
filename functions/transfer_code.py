import yaml

print("moving code into Azure Functions Libraries")

params = yaml.safe_load(open("libs_config.yaml"))

for item in params.keys(): 
    print(item)