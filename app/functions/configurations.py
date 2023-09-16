import yaml
import os

### The goal here is to load as little information as needed. So yaml files are broken into functions. 

def get_configurations():
    configuration = {
        'planet_config':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/planet.yaml")))["planet_types"],
        'moon_config':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/moon.yaml")))["moon_types"],
        'star_config':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/star.yaml")))
    }
    return configuration

def get_homeworld_configurations():
    configuration = {
        'terrestrial':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/terrestrial.yaml"))),
        'species':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/species.yaml"))),
    }
    return configuration

def get_building_configurations():
    configuration = {
        'building':yaml.safe_load(open(os.path.join(os.getenv("abspath"),"app/configurations/buildings.yaml"))),
    }
    return configuration