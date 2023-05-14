import numpy as np

from ..functions import configurations
from ..objects import baseobjects

params = configurations.get_configurations()

class Biome(baseobjects.Baseobject):
    def __init__(self, conf, planet):
        super().__init__()
        self.label = 'biome'
        self.config = conf
        self.matrix_length = self.config.get('matrix_length')
        self.matrix = self.shift_terrain()
        self.onPlanet = planet

    def shift_terrain(self):
        shift = [np.abs(np.round(np.random.normal(
                    1,
                    1,
                    self.matrix_length),0))

            for r in range(self.matrix_length)]
        return shift
    
    def mountain_shift(self, mountain):
        mountain_start = self.get_random_chord()
        for i in mountain.path:
            height = 5
            mountain_start[0]+= i[0]
            mountain_start[1]+= i[1]
            if mountain_start[0] >= self.matrix_length:
                mountain_start[0] = self.matrix_length-1
            if mountain_start[1] >= self.matrix_length:
                mountain_start[1] = self.matrix_length-1     
            if mountain_start[0] < 0:
                mountain_start[0] = 0
            if mountain_start[1] < 0:
                mountain_start[1] = 0   
            self.matrix[mountain_start[0]][mountain_start[1]] += height

    def shift_mountains(self,mountains):
        [self.mountain_shift(mountain) for mountain in mountains]

    def get_random_chord(self):
        x = np.random.choice(self.matrix_length, 1)[0]
        y = np.random.choice(self.matrix_length, 1)[0]
        coord = [x, y]
        return np.array(coord)
    
    def matrix_to_list(self):
        # Longer form [x,y,z,x,y,z,x,y,z,x,y,z,x,y,z,x,y,z,x,y,z,x,y,z]
        np.concatenate([[[x-10,self.matrix[x][z],z-10] for z in range(len(self.matrix))] for x in range(len(self.matrix))]).flatten()

    def flatten_matrix(self):
        # just the `y` axis of the matrix
        return np.array(self.matrix).flatten()

    def get_data(self):
        fund = self.get_fundimentals()
        fund['grid'] = str(self.flatten_matrix())
        return fund

    def get_biome_edge(self):
        edge = {'node1':self.objid,'node2':self.onPlanet['objid'],'label':'isOn'}
        return edge

    def __repr__(self):
        return f"<surface: {self.matrix_length}X{self.matrix_length}>"



class Mountain():
    def __init__(self, conf):
        self.config = conf.get('mountains')
        self.range_length = np.random.randint(self.config['range_length_low'],
                                               high=self.config['range_length_high'])
        self.height = np.round(np.random.normal(loc=self.config['height_avg'],
                                                scale=self.config['heihgt_std'])
                                            ,2)
        self.possible_diretions = [
            [0, 0],
            [1,0],
            [-1,0],
            [0, 1],
            [1,1],
            [-1,1],
            [0,-1],
            [1,-1],
            [-1,-1]
        ]
        self.path_proba = self.set_path_proba()
        self.path = [self.get_random_direction() for i in range(self.range_length)]
        
    def set_path_proba(self):
        rnds = np.random.normal(loc=np.random.choice(range(len(self.possible_diretions))),size=len(self.possible_diretions))
        rnds[rnds<0] = 0
        p = rnds / rnds.sum()
        return p
    
    def get_random_direction(self):
        choice = np.random.choice(range(len(self.possible_diretions)),p=self.path_proba)
        return self.possible_diretions[choice]
                            
    def __repr__(self):
        return f"<mountain: range:{self.range_length}, height:{self.height}>"
    

