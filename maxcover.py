from mip import Model, xsum, maximize, BINARY

class CoveringProblem:
    """ 
    Class that houses the covering problem.
    """

    def __init__(self, xs=31, ys=20):
        self.xs_dim = xs
        self.ys_dim = ys
        self.locations = []
        self.block_size = 1
        self.arrests = []
        self.aij_matrix = []
        
    def fill_locations(self):
        for xloc in range(self.xs_dim):
            for yloc in range(self.ys_dim):
                self.locations.append(Location(xloc * self.block_size, yloc * self.block_size))
                
    def fill_arrests(self):
        for (a_x, a_y, a_id) in ARRESTSPARTB:
            self.arrests.append(CardiacArrest(a_x, a_y, a_id))
            
    
    def get_transposed_aij(self):
        transposed = []
        len_row = self.xs_dim
        for i in range(self.ys_dim):
            row = [(location.id, location.x_pos, location.y_pos) for location in self.locations if location.id // len_row == i]
            transposed.append(row)
            
        return transposed
            
        
        
    def get_aijs(self):
        for arrest in self.arrests:
            location_row = []
            for location in self.locations:
                if arrest.get_location() in location.get_covered():
                    location_row.append(1)
                else:
                    location_row.append(0)
            self.aij_matrix.append(location_row)
        
    

class Location:
    """
    A class that stores properties for all locations.
    """
    __new_id = 0
    
    def __init__(self, x, y):
        self.id = Location.__new_id
        Location.__new_id += 1
        self.x_pos = x
        self.y_pos = y
        self.range = 4
        self.block_size = 1
        
    def get_covered(self):      
        low_x = max(0, self.x_pos - self.range)
        high_x = self.x_pos + self.range + self.block_size
        
        low_y = max(0, self.y_pos - self.range)
        high_y = self.y_pos + self.range + self.block_size
        
        covered_list = []
        
        for x in range(low_x, high_x + self.block_size, self.block_size):
            for y in range(low_y, high_y, self.block_size):
                diff_x = abs(x - self.x_pos)
                diff_y = abs(y - self.y_pos)
                
                if ((diff_x ** 2 + diff_y ** 2 ) ** 0.5) <= self.range:
                    covered_list.append((x, y))
        return covered_list
   
    
class CardiacArrest:    
    def __init__(self, x, y, id_):
        self.x_pos = x
        self.y_pos = y
        self.id = id_
    
    def get_location(self):
        return (self.x_pos, self.y_pos)
        
        
def main():
    N = 2
    
    problem = CoveringProblem()
    problem.fill_locations()
    problem.fill_arrests()
    problem.get_aijs()
    aijs = problem.aij_matrix
    
    #Solving the model
    
    model = Model()
    
    #x indicaties locations
    x = [model.add_var(var_type=BINARY) for location in problem.locations]
    
    #y indicates whether a customer is served or not
    y = [model.add_var(var_type=BINARY) for customer in problem.arrests]
    
    #Objective function
    model.objective = maximize(xsum(y[cid] for cid, customer in enumerate(problem.arrests)))
    
    #Constraints
    for customer in problem.arrests:
        model += y[customer.id - 1] <= xsum(aijs[customer.id - 1][lid] * x[lid] for lid, location in enumerate(problem.locations))
    
    model += xsum(x[lid] for lid, location in enumerate(problem.locations)) == N
    
    model.optimize()
    
    if model.num_solutions:
        print(model.objective_value)
        
    ix = 0
    x_list = []
    for ix in range(31 * 20):
        x_list.append((ix, x[ix].x))
        if x[ix].x == 1:
            print (ix)
    
    print(x_list)
    for location in problem.locations:
        if x[location.id].x == 1:
            print(location.x_pos, location.y_pos)
    
#Arrests are stored as (x, y, id)
ARRESTS = [
    (2, 0, 1),
    (4, 1, 2),
    (5, 1, 3),
    (1, 3, 4),
    (2, 3, 5),
    (3, 3, 6),
    (4, 3, 7),
    (6, 3, 8),
    (2, 4, 9),
    (4, 4, 10),
    (2, 5, 11),
    (6, 6, 12),
    (1, 7, 13),
    (6, 7, 14)
    ]  
    

ARRESTSPARTB = [
    (11,0,1),
    (8,2,2),
    (10,2,3),
    (23,2,4),
    (25,2,5),
    (30,3,6),
    (10,4,7),
    (17,4,8),
    (4,5,9),
    (14,5,10),
    (19,5,11),
    (20,5,12),
    (27,6,13),
    (13,7,14),
    (16,7,15),
    (17,7,16),
    (18,7,17),
    (19,7,18),
    (21,7,19),
    (28,7,20),
    (1,8,21),
    (8,8,22),
    (17,8,23),
    (19,8,24),
    (3,9,25),
    (10,9,26),
    (11,9,27),
    (14,9,28),
    (17,9,29),
    (7,10,30),
    (11,10,31),
    (14,10,32),
    (21,10,33),
    (29,10,34),
    (11,11,35),
    (14,11,36),
    (16,11,37),
    (21,11,38),
    (1,12,39),
    (11,12,40),
    (12,12,41),
    (28,12,42),
    (29,13,43),
    (30,13,44),
    (9,14,45),
    (11,14,46),
    (12,14,47),
    (13,14,48),
    (18,15,49),
    (5,16,50),
    (14,16,51),
    (15,17,52),
    (19,17,53),
    (26,17,54),
    (14,18,55),
    (15,18,56),
    (17,18,57),
    (19,19,58)      
    ]


if __name__ == "__main__":
    main()