# %%
# import sim
import sys
import yaml
import pandas as pd


# %%
# mapping to the modules that make the app
sys.path.insert(0, "..")

from app.creators import homeworld
from app.creators import universe
from app.functions import maths

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
        nodes = pd.concat([pd.DataFrame(i['nodes']) for i in self.systems])
        writer = pd.ExcelWriter('simulation_output.xlsx')
        
        for i in nodes['label'].unique():
            df = nodes[nodes['label']==i]
            df = df.loc[:,df.notna().any(axis=0)]
            df.to_excel(writer, sheet_name=f'{i}_nodes')

        edges = pd.concat([pd.DataFrame(i['edges']) for i in self.systems])
        edges.to_excel(writer, sheet_name=f'edges')
        writer.close()





# %%
def main():
    sim = Simulaiton()
    config = Config()
    print(f"running a simulation on {config.config['simulation']['n_players']} players")
    for iter,item in enumerate(config.sims):
        print(f"generating sim: {iter}")
        # to give forms a random user ID.
        config.user_input['objid'] = maths.uuid()
        config.user_input['accountid'] = maths.uuid()
        sim.systems.append(universe.build_homeSystem(config.user_input, username="simulation"))

    sim.break_down_datasets()

if __name__ == "__main__":
    main()