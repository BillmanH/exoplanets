import numpy as np


class Surface():
    def __init__(self):
        self.matrix_length = 20
        self.matrix = self.shift_terrain()

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


    def get_random_chord(self):
        x = np.random.choice(self.matrix_length, 1)[0]
        y = np.random.choice(self.matrix_length, 1)[0]
        coord = [x, y]
        return np.array(coord)
    
    def get_matrix_gradient(self):
        return np.array(np.gradient(np.array(self.matrix)))[0]
    
    def __repr__(self):
        return f"<surface: {self.matrix_length}X{self.matrix_length}>"



class Mountain():
    def __init__(self):
        self.range_length = 20
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
        rnds = np.array([np.random.uniform(0, 1) for i in self.possible_diretions])
        p = rnds / rnds.sum()
        return p
    
    def get_random_direction(self):
        choice = np.random.choice(range(len(self.possible_diretions)),p=self.path_proba)
        return self.possible_diretions[choice]
                            
    def __repr__(self):
        return f"<mountain: range:{self.range_length}>"
