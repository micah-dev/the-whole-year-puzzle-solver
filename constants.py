import numpy as np

class Board:
    
    def __init__(self, month: str, day: str):
        self.month = month
        self.day = day
        self.month_index = None
        self.day_index = None
        self.str_mask = np.array([
            ["X","X","X","X","X","X","X","X","X"],
            ["X","Jan","Feb","Mar","Apr","May","Jun","X","X"],
            ["X","Jul","Aug","Sep","Oct","Nov","Dec","X","X"],
            ["X","1","2","3","4","5","6","7","X"],
            ["X","8","9","10","11","12","13","14","X"],
            ["X","15","16","17","18","19","20","21","X"],
            ["X","22","23","24","25","26","27","28","X"],
            ["X","X","X","29","30","31","X","X","X"],
            ["X","X","X","X","X","X","X","X","X"],
        ])
        self.mask = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])
        self.solution = np.ones((9,9), dtype=int)
        self.used_shapes = []
        self.set_targets()
        
    def append_used_shape(self, shape_mask, symbol):
        self.used_shapes.append([shape_mask, symbol])
        
    def set_targets(self):
        mx, my = np.where(self.str_mask == self.month)
        dx, dy = np.where(self.str_mask == self.day)
        self.month_index = (mx, my)
        self.day_index = (dx, dy)
        self.mask[mx[0]][my[0]] = 1
        self.mask[dx[0]][dy[0]] = 1

    def display(self):
        print()
        for i in range(self.mask.shape[0]):
            for j in range(self.mask.shape[1]):
                if self.mask[i][j] == 0:
                    v = "⬜"
                if self.mask[i][j] == 1:
                    v = "⬛"
                    
                    if len(self.used_shapes) > 0:
                        for obj in self.used_shapes:
                            mat = obj[0]
                            sym = obj[1]
                            indices = np.argwhere(mat>0)
                            for index in indices:
                                x,y = index
                                if x == i and y == j:
                                    v = sym
                    
                if self.month_index is not None and self.day_index is not None:
                    if i == self.month_index[0] and j == self.month_index[1]:
                        v = "🎯"
                    if i == self.day_index[0] and j == self.day_index[1]:
                        v = "🎯"
                print(v, end='')
            print()
        print()

class Shape:
    def __init__(self, mat: np.array, sym: str):
        self.mat = mat
        self.sym = sym
        self.rots = None
        self.inv = 1 - mat
        self.curr_xy = None
        
    def get_rots(self):
        s = self.mat
        rots = []
        rots.append(s)
        rots.append(np.rot90(s, k=1))
        rots.append(np.rot90(s, k=2))
        rots.append(np.rot90(s, k=3))
        fs = np.flipud(s)
        rots.append(fs)
        rots.append(np.rot90(fs, k=1))
        rots.append(np.rot90(fs, k=2))
        rots.append(np.rot90(fs, k=3))

        seen = set([])
        unique_rots = []
        for j in rots:
            f = tuple(list(j.flatten()))
            if f not in seen:
                unique_rots.append(j)
                seen.add(f)

        data = []
        for urot in unique_rots:
            data.append(Shape(urot, self.sym))
        return data
    
    def display(self):
        print()
        for i in range(self.mat.shape[0]):
            for j in range(self.mat.shape[1]):
                if self.mat[i][j] == 0:
                    v = "⬜"
                if self.mat[i][j] == 1:
                    v = self.sym 
                print(v, end='')
            print()
        print()

SHAPES = [
    Shape(np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ]), "🟪" # 0 # Plus # 9 Placements, 1 Unique Rotation
    ),
    Shape(np.array([
            [1, 1],
            [1, 1],
        ]), "🧱" # 1 # Square # 23 Placements, 1 Unique Rotation
    ),
    Shape(np.array([
            [1, 0],
            [1, 1],
            [0, 1],
        ]), "🟦" # 2 # Bolt # 46 Placements, 3 Unique Rotation
    ),
    Shape(np.array([
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1],
        ]), "⏹️" # 3 # Snake # 46 Placements, 4 Unique Rotation
    ),
    Shape(np.array([
            [1, 1],
            [0, 1],
            [1, 1],
        ]), "🟨" # 4 # Cup # 51 Placements, 4 Unique Rotations
    ),
    Shape(np.array([
            [0, 1],
            [1, 1],
            [0, 1],
        ]), "🟫" # 5 # Cup # 60 Placements, 4 Unique Rotations
    ),
    Shape(np.array([
            [1, 1],
            [1, 1],
            [0, 1],
        ]), "🟧" # 6 # Chair # 91 Placements, 6 Unique Rotations
    ),
    Shape(np.array([
            [1, 1],
            [0, 1],
            [0, 1],
        ]), "🟥" # 7 # Small L # 99 Placements, 8 Unique Rotations
    ),
    Shape(np.array([
            [1, 1],
            [0, 1],
            [0, 1],
            [0, 1],
        ]), "🟩" # 8 # Big L # 135 Placements, 8 Unique Rotations
    ),
    
]

BAD_PATTERNS = [
    
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    
    np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]),
    np.array([
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ]),
    np.array([
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ]),
    np.array([
        [0, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 0],
    ]),
    
    np.array([
        [1, 1, 0],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 0],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    
    np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]),
    
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
    ]),
    
    
    
    np.array([
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ]),
    np.array([
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0],
    ]),
    np.array([
        [0, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 0],
    ]),
    np.array([
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [0, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]),
    np.array([
        [0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
    ]),
    np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 0],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0],
    ]),
    
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 1, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 1],
    ]),

    np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]),
    np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]),
]