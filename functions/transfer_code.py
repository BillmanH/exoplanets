
import yaml
import shutil
import os

print("moving code into Azure Functions Libraries")

params = yaml.safe_load(open("libs_config.yaml"))

for item in params['used_from_lib'].keys(): 
    print(item)
    for subitem in params['used_from_lib'][item].keys():
        print(" ",subitem)
        for file in params['used_from_lib'][item][subitem]:
            print("     ",file)
            shutil.copyfile(os.path.join(f"../app/{subitem}/{file}"),
                            os.path.join(f"{item}/app/{subitem}/{file}")
                            )