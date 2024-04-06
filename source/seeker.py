import numpy
from Map import Map
from MoveAction import MoveAction
import random

import queue

class Seeker:
    def __init__(self, pos, vissionRange):
        self.visionGrid = None
        self.mapGrid = None
        self.rowPos = pos[0]
        self.colPos = pos[1]
        self.visionRange = vissionRange
        self.catched = 0
        self.sight = {}
        self.numberOfSteps = 0
        self.priorityTarget = None
        self.targetList = {"hider": {}, "ping": {}, "random": []}
        self.pathToTarget = []
        self.score = 0
        self.visitedPosList = {(0, 0)}
        self.visitedPosSightList = {(0, 0)}

    def calcScore(self):
        self.score = self.catched * 20 + self.numberOfSteps


    def setNumberOfSteps(self, numberOfSteps):
        self.numberOfSteps = numberOfSteps


    def getPriorityTarget(self):
        minDist = 100000
        priorityTarget = None
        for hiderPos in self.targetList["hider"].values():
            dist = self.get_heuristic((self.rowPos, self.colPos), hiderPos)
            if dist < minDist:
                minDist = dist
                priorityTarget = hiderPos
        if minDist != 100000:
            return priorityTarget
        
        for pingPos in self.targetList["ping"].values():
            if pingPos in self.visitedPosList:
                continue
            dist = self.get_heuristic((self.rowPos, self.colPos), pingPos)
            if dist < minDist:
                minDist = dist
                priorityTarget = pingPos
        if minDist == 100000:
            movablePosition = []
            for r in range(1, self.mapGrid.shape[0] - 1):
                for c in range(1, self.mapGrid.shape[1] - 1):
                    if self.mapGrid[r, c] == 0 and (r, c) not in self.visitedPosSightList:
                        movablePosition.append((r, c))
            if movablePosition:
                self.visitedPosSightList.clear()
                for r in range(1, self.mapGrid.shape[0] - 1):
                    for c in range(1, self.mapGrid.shape[1] - 1):
                        if self.mapGrid[r, c] == 0 and (r, c) not in self.visitedPosList:
                            movablePosition.append((r, c))
                
            priorityTarget = random.choice(movablePosition)
        return priorityTarget

    def sendPosition(self):
        return (self.rowPos, self.colPos)

    def setupBefore_priorityTarget(self, map : Map):
        if map.hidersList and map.hidersList[0].isChangePingPos():
            self.targetList["ping"].clear()
            for hider in map.hidersList:
                self.targetList["ping"][hider.id] = hider.sendPingPos(map)
                

    def setupAfter_priorityTarget(self, map : Map):
        for hiderid, pingPos in self.targetList["ping"].items():
            if self.rowPos == pingPos[0] and self.colPos == pingPos[1]:
                self.targetList["ping"].pop(hiderid)
                break
    
        hiderInSight = map.getHiderInSeekerSight()
        if hiderInSight:
            for hider in hiderInSight:
                self.targetList["hider"][hider.id] = hider.sendPosition()
        else:
            self.targetList["hider"].clear()
                

        print("target list: ", self.targetList)
        
        print(f"priority target: {self.getPriorityTarget()}")

    def get_catched(self):
        return self.catched

    def getSight(self, map : Map):
        self.sight = map.getSeekerSight()
        self.visitedPosSightList.update(self.sight)
        return self.sight


    def getDirec_random(self):
        listPossibleMove = [MoveAction.UP, MoveAction.DOWN, MoveAction.LEFT, MoveAction.RIGHT, MoveAction.UP_LEFT, MoveAction.UP_RIGHT, MoveAction.DOWN_LEFT, MoveAction.DOWN_RIGHT]
        #check the first around from the seeker
        for direction in listPossibleMove[:]:
            r, c = self.rowPos + direction.value[0], self.colPos + direction.value[1]
            if self.mapGrid[r][c] == 1:
                listPossibleMove.remove(direction)
        
        return random.choice(listPossibleMove)
    
    def getDirec_followPing(self, listPossibleMove):
        pass

    
    
    def catchHiderHandler(self, map : Map):
        for hider in map.hidersList:
            if (self.rowPos, self.colPos) == hider.sendPosition():

                self.catched += 1
                self.targetList["hider"].pop(hider.id)
                map.hidersList.remove(hider)
                print("catched hider")
                break




    def AStarAlgorithm(self, map : Map, init_pos, target_pos):
        frontier = queue.PriorityQueue()
        frontier.put((self.get_heuristic(init_pos, target_pos), init_pos))
        reached = []
        parents = {}
        parents[init_pos] = None
        while not frontier.empty():
            node = frontier.get()
            step, pos = node
            reached.append(pos)
            if pos == target_pos:
                return parents
            listMoveAction = self.get_possibleMoveActions(map, pos)
            for moveAction in listMoveAction:
                new_pos = (pos[0] + moveAction.value[0], pos[1] + moveAction.value[1])
                if new_pos not in reached :
                    reached.append(new_pos)
                    parents[new_pos] = pos
                    priority = self.get_heuristic(new_pos, target_pos) + 1 + step
                    frontier.put((priority, new_pos))
        return None

    def get_possibleMoveActions(self, map:Map, pos:tuple[int, int]):
        listPossibleMove = [MoveAction.UP, MoveAction.DOWN, MoveAction.LEFT, MoveAction.RIGHT, MoveAction.UP_LEFT, MoveAction.UP_RIGHT, MoveAction.DOWN_LEFT, MoveAction.DOWN_RIGHT]
        for direction in listPossibleMove[:]:
            r, c = pos[0] + direction.value[0], pos[1] + direction.value[1]
            if map.grid[r][c] == 1:
                listPossibleMove.remove(direction)
        return listPossibleMove
    
    def get_heuristic(self, pos:tuple[int, int], target_pos:tuple[int, int]):
        dist = max(abs(target_pos[0] - pos[0]), abs(target_pos[1] - pos[1]))
        return dist
    
    def getPathToTarget(self, map : Map, init_pos, target_pos):
        if target_pos is None:
            return None
        parents = self.AStarAlgorithm(map, init_pos, target_pos)
        if parents is None:
            return None
        path = []
        while target_pos is not None:
            path.append(target_pos)
            target_pos = parents[target_pos]
        return path

    def getDirectFromAstarAlgorithm(self, initPos):
        if self.pathToTarget is None or len(self.pathToTarget) < 2:
            print("No path to target")
            return MoveAction.STAY
        next_pos = self.pathToTarget[len(self.pathToTarget) - 2]
        moveAction_tuple = (next_pos[0] - initPos[0], next_pos[1] - initPos[1])
        return MoveAction.get_fromTuple(moveAction_tuple)
        

    def getMoveDirection(self):
        moveAction = self.getDirectFromAstarAlgorithm((self.rowPos, self.colPos))
        return moveAction
    
    def move(self, map : Map):
        self.getSight(map)

        self.setupBefore_priorityTarget(map)

        self.pathToTarget = self.getPathToTarget(map, (self.rowPos, self.colPos), self.getPriorityTarget())
        moveAction = self.getMoveDirection()

        self.rowPos += moveAction.value[0]
        self.colPos += moveAction.value[1]

        self.visitedPosSightList.add((self.rowPos, self.colPos))
        self.visitedPosList.add((self.rowPos, self.colPos))

        self.setupAfter_priorityTarget(map)

        self.catchHiderHandler(map)



    def move_decision(self):
        pass


    def detect_hider(self):
        pass

    def update_score(self):
        pass

    



    