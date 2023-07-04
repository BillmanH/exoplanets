# %%
import sim
import sys
import yaml
import pandas as pd

# %%
# mapping to the modules that make the app
sys.path.insert(0, "..")

from app.creators import homeworld
from app.creators import universe
# %%


class Config:
    def __init__(self) -> None:
        self.config = yaml.safe_load(open("sim_config.yaml"))
        self.user_input = self.config['userform']
        self.sims = range(self.config['simulation']['n_players'])


class Simulaiton:
    def __init__(self) -> None:
        self.systems = []

    def break_down_datasets(self):
        nodes = pd.concat([pd.DataFrame(i['nodes']) for i in sim.systems])

# %%
def main():
    sim = Simulaiton()
    config = Config()
    print(f"running a simulation on {config.config['simulation']['n_players']} players")
    for iter,item in enumerate(config.sims):
        print(f"generating sim: {iter}")
        sim.systems.append(universe.build_homeSystem(config.user_input, username="simulation"))

    nodes = pd.concat([pd.DataFrame(i['nodes']) for i in sim.systems])
    nodes.reset_index(drop=False).to_csv('simulation_nodes_out.csv')
    edges = pd.concat([pd.DataFrame(i['edges']) for i in sim.systems])
    edges.reset_index(drop=False).to_csv('simulation_edges_out.csv')

if __name__ == "__main__":
    main()