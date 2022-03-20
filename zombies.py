"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        self._obs_list = []
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
                self._obs_list.append(cell)
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in list(self._zombie_list):
            yield zombie
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in list(self._human_list):
            yield human
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        
        distance_field = [[(self.get_grid_height() * self.get_grid_width()) for dummy_col in range(self.get_grid_width())] 
                          for dummy_row in range(self.get_grid_height())]
        
        boundary = poc_queue.Queue()
        
        wanted = []
        if entity_type == ZOMBIE:
            wanted = list(self._zombie_list)
        elif entity_type == HUMAN:
            wanted = list(self._human_list)        
        for item in wanted:
            boundary.enqueue(item)
            
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
            
        while len(boundary) > 0:
            current = boundary.dequeue()
            #if entity_type == ZOMBIE:
            neighbor_cells = self.four_neighbors(current[0], current[1])
            #elif entity_type == HUMAN:
                #neighbor_cells = self.eight_neighbors(current[0], current[1])
            for nei_cell in neighbor_cells:
                if visited.is_empty(nei_cell[0], nei_cell[1]) and nei_cell not in self._obs_list:
                    visited.set_full(nei_cell[0], nei_cell[1])
                    boundary.enqueue(nei_cell)
                    distance_field[nei_cell[0]][nei_cell[1]] = (distance_field[current[0]][current[1]] + 1)
        
#        for row in range(self.get_grid_height()):
#            print distance_field[row]
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        nei_cells = []
        max_dist = 0
        new_list = []
        for human in list(self._human_list):
            max_dist = 0
            nei_cells = []
            nei_cells = self.eight_neighbors(human[0], human[1])
            nei_cells.append(human)
            for cell in nei_cells:
                if zombie_distance_field[cell[0]][cell[1]] > max_dist and self.is_empty(cell[0], cell[1]):
                    max_dist = zombie_distance_field[cell[0]][cell[1]]
                    max_cell = cell
            new_list.append(max_cell)
        #print self    
        #print new_list, self._obs_list     
        self._human_list = new_list
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        nei_cells = []
        min_dist = float('inf')
        new_list = []
        min_cell = (0, 0)
        for zombie in list(self._zombie_list):
            min_dist = float('inf')
            nei_cells = []
            nei_cells = self.four_neighbors(zombie[0], zombie[1])
            nei_cells.append(zombie)
            for cell in nei_cells:
                if human_distance_field[cell[0]][cell[1]] < min_dist and self.is_empty(cell[0], cell[1]):
                    min_dist = human_distance_field[cell[0]][cell[1]]
                    min_cell = cell
            new_list.append(min_cell)
        #print self    
        #print new_list  
        self._zombie_list = new_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
#obj = Apocalypse(3, 3, [], [], [(2, 2)]) 
#obj.compute_distance_field(HUMAN)
#obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)])
#obj.compute_distance_field(HUMAN)
#obj = Apocalypse(3, 3, [], [(2, 2)], [(1, 1)]) 
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]] 
#obj.move_humans(dist)
#obj = Apocalypse(3, 3, [], [(1, 1)], [(1, 1)])
#dist = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
#obj.move_zombies(dist)
#poc_zombie_gui.run_gui(Apocalypse(30, 40))
