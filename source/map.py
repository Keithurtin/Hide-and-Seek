import numpy as np
import random
from pathlib import Path
from termcolor import colored

class Map:

    def __init__(self) -> None:
        self.seeker_pos = None
        self.hider_pos = []
        self.numOfHider = 0
        self.obstacle = []

    # Function to read a map from folder maps 
    def read_map(self):
        filename = input("Choose a map in folder \"maps\": ")
        root = Path(__file__).parents[1]
        _path = root / (r"maps/" + filename)
        with open(_path, 'r') as f:
            self.row, self.col = [int(x) for x in next(f).split()]
            self.row += 2
            self.col += 2
            self.grid = np.empty((self.row, self.col), 'i')
            self.create_map_boundary()
            r = 1
            for line in f:
                if (r < self.row - 1):
                    arr = np.array([int(x) for x in line.split()])
                    for c in range(1, self.col - 1):
                        self.grid[r, c] = arr[c - 1]
                        if (self.grid[r, c] == 2):
                            self.hider_pos.append((r, c))
                            self.numOfHider += 1
                        if (self.grid[r, c] == 3):
                            self.seeker_pos = (r, c)
                    r += 1
                else:
                    top, left, bottom, right = [int(x) for x in line.split()]
                    top += 1
                    left += 1
                    bottom += 1
                    right += 1
                    self.obstacle.append((top, left, bottom, right))
                    for i in range (top, bottom + 1):
                        for j in range(left, right + 1):
                            self.grid[i, j] = 1

    def create_map_boundary(self):
        for i in range(self.row):
            self.grid[i, 0] = 1
            self.grid[i, self.col - 1] = 1
        for i in range(self.col):
            self.grid[0, i] = 1
            self.grid[self.row - 1, i] = 1

    def print_map(self):
        for i in range(self.row):
            for j in range(self.col):
                if (self.grid[i, j] == 3):
                    print(colored(3, 'red'), end = " ")
                elif (self.grid[i, j] == 2):
                    print(colored(2, 'blue'), end = " ")
                elif (self.grid[i, j] == 9):
                    print(colored(0, 'yellow'), end = " ")
                    self.grid[i, j] = 0
                else:
                    print(self.grid[i, j], end = " ")
            print('\n')

    # Function to get visible cells of seeker/hiders
    def get_vision(self, agent):
        x, y = agent.row, agent.col
        vi_range = agent.vision_range
        visible_cells = []

        top = max(0, x - vi_range)
        bottom = min(self.row, x + vi_range + 1)
        left = max(0, y - vi_range)
        right = min(self.col, y + vi_range + 1)

        for i in range(top, bottom):
            for j in range(left, right):
                if (self.grid[i, j] != 1):
                    if (self.is_visible(x, y, i, j)):
                        visible_cells.append((i, j))
        return visible_cells

    def is_visible(self, x0, y0, x1, y1):
        route = self.bresenham(x0, y0, x1, y1)
        for cell in route:
            if (self.grid[cell[0], cell[1]] == 1):
                return False
        return True

    # Function return cells that are crossed when going from point A to point B
    # If there is any cell which is wall or obstacle on this route, unit stands at 
    # point A cannot see unit stands at point B
    # This function is constructed base on Brasenham's line algorithm
    # For more information, see https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
    def bresenham(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0
        result = []
        for x in range(dx + 1):
            
            result.append(np.array([x0 + x * xx + y * yx, y0 + x * xy + y * yy], 'i'))

            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy 
        return np.array(result, 'i')
    
    # Function to announce the position of hiders
    def ping_hider(self):
        ping_list = []
        for hider in self.hider_pos:
            top = max(0, hider[0] - 3)
            bottom = min(self.row - 1, hider[0] + 3)
            left = max(0, hider[1] - 3)
            right = min(self.col - 1, hider[1] + 3)

            while True:
                x = random.randint(top, bottom)
                y = random.randint(left, right)
                if (self.grid[x, y] == 0):
                    ping_list.append((x, y))
                    self.grid[x, y] = 9
                    break
        return ping_list
    
    def delete_ping(self, ping_list):
        for ping in ping_list:
            self.grid[ping[0], ping[1]] = 0


