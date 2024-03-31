from map import *
from main import cal_dist


class Hider:

    def __init__(self, row, col, vision_range=2) -> None:
        self.row = row
        self.col = col
        self.vision_range = vision_range
        self.visited_cells = set()

    def get_visible_cells(self, map: Map):
        visible_cells = []
        for i in range(max(0, self.row - self.vision_range), min(map.row, self.row + self.vision_range + 1)):
            for j in range(max(0, self.col - self.vision_range), min(map.col, self.col + self.vision_range + 1)):
                if map.grid[i, j] != 1 and map.is_visible(self.row, self.col, i, j):
                    visible_cells.append((i, j))
                    self.visited_cells.add((i, j))
        return visible_cells

    def is_good_position(self, map: Map, visible_cells):
        for pos in visible_cells:
            if map.grid[pos[0], pos[1]] == 3:
                return False
        return True

    def move(self, map: Map):
        visible_cells = self.get_visible_cells(map)
        safe_cells = [
            cell for cell in visible_cells if cell not in map.seeker_pos]
        if self.is_good_position(map, visible_cells):
            return 0
        if safe_cells:
            seeker_pos = map.seeker_pos
            max_distance = 0
            furthest_cell = None

            for cell in safe_cells:
                distance = cal_dist(cell, seeker_pos)
                if distance > max_distance:
                    max_distance = distance
                    furthest_cell = cell

            if furthest_cell is not None and map.grid[furthest_cell[0], furthest_cell[1]] != 1:
                map.grid[self.row, self.col] = 0
                self.row, self.col = furthest_cell
                map.grid[self.row, self.col] = 2
        return 1
