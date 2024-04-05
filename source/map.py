import numpy   
import random
from pathlib import Path
from termcolor import colored
from MoveAction import MoveAction
import os
# from Seeker import Seeker


class Map:
    def __init__(self, fileName):
        self.fileName = fileName
        self.seekerPosition = None
        self.hiderPosList = []
        self.numOfHider = 0
        self.obstacle = []
        self.grid = None
        self.rowsNum = 0
        self.colsNum = 0
        self.pingPosList = {}
        self.hidersList = []
        self.seeker = None
        self.numberOfSteps = 0
        self.isNewPing = False
        self.load_map_from_file()

    def isSafe(self, pos):
        if (self.grid[pos[0], pos[1]] != 0):
            return False
        for hider in self.hidersList:
            if (hider.sendPosition() == pos):
                return False
        return True
        
    def setNumberOfSteps(self, numberOfSteps):
        self.numberOfSteps = numberOfSteps

    def load_map_from_file(self):
        origin_grid = None
        with open(self.fileName, 'r') as f:
            self.rowsNum, self.colsNum = map(int, f.readline().split())

            origin_grid = numpy.loadtxt(f, dtype=int, max_rows=self.rowsNum)

            for line in f:
                if line.strip() != '':
                    self.obstacle.append(tuple(map(int, line.split())))
            
            #wrap the map with ones
            self.grid = numpy.ones((self.rowsNum + 2, self.colsNum + 2), dtype=int)
            self.grid[1:-1, 1:-1] = origin_grid
            
            self.rowsNum += 2
            self.colsNum += 2

        for r in range(1, self.rowsNum - 1):
            for c in range(1, self.colsNum - 1):
                if (self.grid[r, c] == 2):
                    self.hiderPosList.append((r, c))
                    self.numOfHider += 1
                if (self.grid[r, c] == 3):
                    self.seekerPosition = (r, c)
        
        for top, left, bottom, right in self.obstacle:
            top += 1
            left += 1
            bottom += 1
            right += 1
            for i in range(top, bottom + 1):
                for j in range(left, right + 1):
                    self.grid[i, j] = 1

    def addHider(self, hider):
        self.hidersList.append(hider)

    def addSeeker(self, seeker):
        self.seeker = seeker    
        self.seeker.mapGrid = self.grid
                    
    def receiveHiderPosition(self, hiderPosition):
        if (hiderPosition not in self.hiderPosList):
            self.hiderPosList.append(hiderPosition)
            self.numOfHider += 1

    
    def getHiderInSeekerSight(self):
        hiderInSightList = []
        seekerSight = self.getSeekerSight()
        for hider in self.hidersList:
            if (hider.sendPosition() in seekerSight):
                hiderInSightList.append(hider)
        return hiderInSightList

    def getSeekerAndHidersInfo(self):
        return self.seekerPosition, self.hiderPosList, self.numOfHider
    
    def getHiderSight(self, hider):
        x, y = hider.sendPosition()
        visibleCells = []
        visionRange = hider.visionRange
        top = max(0, x - visionRange)
        bottom = min(self.rowsNum, x + visionRange + 1)
        left = max(0, y - visionRange)
        right = min(self.colsNum, y + visionRange + 1)

        for i in range(top, bottom):
            for j in range(left, right):
                if (self.grid[i, j] != 1):
                    if (self.is_visible(x, y, i, j)):
                        visibleCells.append((i, j))
        return visibleCells
    
    def getSeekerSight(self):
        x, y = self.seeker.sendPosition()
        visibleCells = []
        visionRange = self.seeker.visionRange
        top = max(0, x - visionRange)
        bottom = min(self.rowsNum, x + visionRange + 1)
        left = max(0, y - visionRange)
        right = min(self.colsNum, y + visionRange + 1)

        for i in range(top, bottom):
            for j in range(left, right):
                if (self.grid[i, j] != 1):
                    if (self.is_visible(x, y, i, j)):
                        visibleCells.append((i, j))
        return visibleCells
    
    def getHiderPingPos(self, hider, pingRange = 3):
        hiderPos = hider.sendPosition()
        possiblePingPos = []
        for i in range(-pingRange + 1, pingRange):
            for j in range(-pingRange + 1, pingRange):
                if (i, j) != (0, 0) and self.grid[hiderPos[0] + i, hiderPos[1] + j] != 1:
                    possiblePingPos.append((hiderPos[0] + i, hiderPos[1] + j))
        pingPos = random.choice(possiblePingPos)
        return pingPos
            

    def getRandomPos(self):
        possiblePos = []
        for i in range(1, self.rowsNum - 1):
            for j in range(1, self.colsNum - 1):
                if (self.grid[i, j] == 0):
                    possiblePos.append((i, j))
        return random.choice(possiblePos)
    
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

            result.append(
                numpy.array([x0 + x * xx + y * yx, y0 + x * xy + y * yy], 'i'))

            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
        return numpy.array(result, 'i')

    def updateMapGrid(self):
        for i in range(self.rowsNum):
            for j in range(self.colsNum):
                if (self.grid[i,j] != 1):
                    self.grid[i,j] = 0

        for hider in self.hidersList:
            self.grid[hider.sendPosition()[0], hider.sendPosition()[1]] = 2
            pingPos = hider.sendPingPos(self)
            if hider.id in self.seeker.targetList["ping"]:
                self.grid[pingPos[0], pingPos[1]] = 9

        self.grid[self.seeker.sendPosition()[0], self.seeker.sendPosition()[1]] = 3

    def display_map(self):
        
        self.updateMapGrid()

        for i in range(self.rowsNum):
            for j in range(self.colsNum):
                if (self.grid[i, j] == 1):
                    print(colored('X', 'red'), end=' ')
                elif (self.grid[i, j] == 2):
                    print(colored('H', 'green'), end=' ')
                elif (self.grid[i, j] == 3):
                    print(colored('S', 'blue'), end=' ')
                elif (self.grid[i, j] == 9):
                    print(colored('P', 'yellow'), end=' ')
                else:
                    print(' ', end=' ')
            print()
        
        print(self.seeker.sendPosition())
        for hider in self.hidersList:
            print(hider.sendPosition())