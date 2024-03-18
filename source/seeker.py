import random
from queue import PriorityQueue
from map import *

class Seeker:

    def __init__(self, row, col, vision_range) -> None:
        self.row, self.col = row, col
        self.vision_range = vision_range
        self.catched = 0
        self.visited_node = {}
        self.sight = {}
        self.moves = {}
        self.priority_target = None
        self.target_aim = False
        self.observed_list = []

    # Get a list of visible cells of seeker
    def get_sight(self, map):
        pos = (self.row, self.col)
        if pos in self.visited_node:
            return self.sight[pos]
        
        vision = map.get_vision(self)
        self.sight[pos] = vision
        for cell in vision:
            if cell not in self.observed_list:
                self.observed_list.append(cell)
        return vision

    # Generate all possible move seeker can take
    def get_possible_move(self, map, pos):
        if pos in self.visited_node:
            return self.moves[pos]
        
        row_list = [0, 0, 1, -1, 1, 1, -1, -1]
        col_list = [1, -1, 0, 0, 1, -1, 1, -1]
        moves_list = []

        for k in range(8):
            new_pos = (pos[0] + row_list[k], pos[1] + col_list[k])
            if (new_pos[0] > 0 and new_pos[0] < map.row and new_pos[1] > 0 and new_pos[1] < map.col and map.grid[new_pos[0], new_pos[1]] != 1):
                moves_list.append(new_pos)
        self.moves[pos] = moves_list
        return moves_list
    
    def move(self, map, pos):
        if (map.grid[pos[0], pos[1]] == 2): 
            self.catched += 1
            for hider in map.hider_pos:
                if (hider == pos):
                    map.hider_pos.remove(hider)
            self.target_aim =  False
        map.grid[self.row, self.col] = 0
        self.row = pos[0]
        self.col = pos[1]
        self.get_sight(map)
        map.grid[self.row, self.col] = 3

    # Seeker moves randomly
    def wander(self, map):
        moves_list = self.get_possible_move(map, (self.row, self.col))
        pos = random.choice(moves_list)
        self.move(map, pos)

    def chase(self, map):
        pq = PriorityQueue()
        parents = {}
        expanded = []
        pq.put((0, (self.row, self.col)))
        parents[(self.row, self.col)] = (0, 0)
        while not pq.empty():
            node = pq.get()
            step = node[0]
            pos = node[1]
            expanded.append(pos)
            if (pos == self.priority_target):
                return parents
            possible_moves = self.get_possible_move(map, pos)
            for new_pos in possible_moves:
                if not new_pos in expanded:
                    expanded.append(new_pos)
                    parents[new_pos] = pos
                    priority = step + 1 + self.get_heuristic(new_pos)
                    pq.put((priority, new_pos))

    def get_heuristic(self, pos):
        dist = max(abs(self.priority_target[0] - pos[0]), abs(self.priority_target[1] - pos[1]))
        return dist

    def backtrack(self, parents, pos):
        route = []
        while(parents[pos] != (0, 0)):
            route.append(pos)
            pos = parents[pos]
        route.reverse()
        return route
    
    # Search around a position with a specific range
    def search_around(self, map, pos):
        top = max(0, pos[0] - 3)
        bottom = min (map.row, pos[0] + 4)
        left = max(0, pos[1] - 3)
        right = min(map.col, pos[1] + 4)
        unobserved_list = []

        for i in range(top, bottom):
            for j in range(left, right):
                pos = (i, j)
                if (map.grid[i, j] != 1) and (pos not in self.observed_list):
                    unobserved_list.append(pos)
        return unobserved_list

        