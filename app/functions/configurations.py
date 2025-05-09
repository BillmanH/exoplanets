import yaml
import os

### The goal here is to load as little information as needed. So yaml files are broken into functions. 
### This way, we can load only what we need at the time.
abs_path = os.getenv("ABS_PATH",".")

def get_configurations():
    celestials_config = yaml.safe_load(open(os.path.join(abs_path,"app/configurations/celestials.yaml")))
    configuration = {
        'planet_config':celestials_config["planets"],
        'moon_config':celestials_config["moons"],
        'star_config':celestials_config["stars"],
        'asteroid_config':celestials_config["asteroids"],
        'resource_config':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/resources.yaml")))
    }
    configuration = add_atmosphere_configurations(configuration)
    return configuration

def get_homeworld_configurations():
    configuration = {
        'terrestrial':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/terrestrial.yaml"))),
        'species':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/species.yaml"))),
    }
    return configuration

def get_building_configurations():
    configuration = {
        'building':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/buildings.yaml"))),
    }
    return configuration

def get_resource_configurations():
    configuration = {
        'resource':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/resources.yaml"))),
    }
    return configuration

def get_ship_configurations():
    configuration = {
        'ship':yaml.safe_load(open(os.path.join(abs_path,"app/configurations/ships.yaml"))),
    }
    return configuration


def add_atmosphere_configurations(configuration):
    atmosphere_config = yaml.safe_load(open(os.path.join(abs_path,"app/configurations/atmospheres.yaml")))
    for item in configuration['planet_config'].keys():
        if configuration['planet_config'][item]['has_atmosphere']:
            configuration['planet_config'][item]['atmosphere'] = atmosphere_config
    return configuration