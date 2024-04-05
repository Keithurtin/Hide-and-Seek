from Seeker import Seeker
import random

class Hider:
    def __init__(self, id, seeker:Seeker, pos:tuple[int, int], pingResetInterval, visionRange, map):
        self.pos = pos
        self.is_caught = False
        self.pingPos = None
        self.tmpPingPos = 0
        self.isSetPingPos = False
        self.pingResetInterval = pingResetInterval
        self.numberOfSteps = 0
        self.id = id
        self.visionRange = visionRange
        self.sight = {}

        map.addHider(self)

    def setNumberOfSteps(self, numberOfSteps):
        self.numberOfSteps = numberOfSteps

    def sendPosition(self):
        return self.pos

    def sendPingPos(self, map):
        if (self.numberOfSteps - 1) % self.pingResetInterval == 0:
            if self.tmpPingPos == 0:
                self.pingPos = map.getHiderPingPos(self)
                self.tmpPingPos += 1
        else:
            self.tmpPingPos = 0
        return self.pingPos
    
    def isChangePingPos(self):
        if (self.numberOfSteps - 1) % self.pingResetInterval == 0:
            self.isSetPingPos = True
        else:
            self.isSetPingPos = False
        return self.isSetPingPos
    
    def getSight(self, map):
        self.sight = map.getHiderSight(self)
    

    def move(self, map):
        self.getSight(map)
        seeker_position = map.seeker.sendPosition()
        if seeker_position in self.sight:
            safe_moves = []
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                if map.isSafe(new_pos):
                    safe_moves.append(new_pos)

            if safe_moves:
                new_position = random.choice(safe_moves)
                self.pos = new_position



    