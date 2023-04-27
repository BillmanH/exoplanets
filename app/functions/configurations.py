import yaml
import os

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
    }
    return configuration