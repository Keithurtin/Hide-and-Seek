from GameState import GameState
from GameObjectFactory import GameObjectFactory
from GameObject import GameObject
from GlobalInfo import GlobalInfo
from GameStateMachine import GameStateMachine
from EndGameState import EndGameState

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Map import Map
from Seeker import Seeker
from Hider import Hider
import os
import pygame

CELL_SIZE = 40
WHITE = (255, 255, 255)
PINK = (238, 162, 173, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



class PlayGameState(GameState):
    def __init__(self):
        self._playID = "PLAY"
        self.gameObjectFactory = GameObjectFactory()
        self.mapGame = None
        self.seeker = None
        self.level = 0
        self.hiderList = []

        self.totalHider = 0

        self.countFrame = 0

    def update(self):
        if self.countFrame % 15 == 0:    
            self.mapGame.setNumberOfSteps(self.numberOfSteps)
            for hider in self.hiderList:
                hider.setNumberOfSteps(self.numberOfSteps)
            self.seeker.setNumberOfSteps(self.numberOfSteps)

            if self.level == 3:
                for hider in self.hiderList:
                    hider.move(self.mapGame)
            self.seeker.move(self.mapGame)
            self.mapGame.display_map()
            self.numberOfSteps += 1
            GlobalInfo.Instance().setGlobalInfo("numberOfSteps", self.numberOfSteps)
            GlobalInfo.Instance().setGlobalInfo("score", self.seeker.get_catched() * 20 - self.numberOfSteps)

            # print(f"Number of steps: {self.numberOfSteps}")
            
    def render(self):
        self.subScreen.fill(WHITE)
        self.disPlayMapGui(self.subScreen)
        pygame.display.flip()
            
        self.countFrame += 1

        if self.seeker.get_catched() == len(self.hiderList):
            GameStateMachine.Instance().changeState(EndGameState())
        

    def handleEvents(self, event):
        
        pass

    def onEnter(self):
        pathToAssets = Path(__file__).parents[2] / "asset"

        hiderImg = pygame.image.load(pathToAssets / "human.png")
        self.hiderPNG = pygame.transform.scale(hiderImg, (CELL_SIZE, CELL_SIZE))
        seekerImg = pygame.image.load(pathToAssets / "monster.png")
        self.seekerPNG = pygame.transform.scale(seekerImg, (CELL_SIZE, CELL_SIZE))
        wallImg = pygame.image.load(pathToAssets / "wall.png")
        self.wallPNG = pygame.transform.scale(wallImg, (CELL_SIZE, CELL_SIZE))
        pingImg = pygame.image.load(pathToAssets / "ping.png")
        self.pingPNG = pygame.transform.scale(pingImg, (CELL_SIZE, CELL_SIZE))

        mapFileName = GlobalInfo.Instance().getGlobalInfo("inputMap_box")
        self.level = int(GlobalInfo.Instance().getGlobalInfo("inputLevel_box"))
        pingResetInterval = int(GlobalInfo.Instance().getGlobalInfo("inputPingReset_box"))
        pathToMap = Path(__file__).parents[2] / "maps" 
        self.mapGame = Map(fileName=pathToMap / mapFileName)
        seeker_pos, hider_pos_list, numOfHider = self.mapGame.getSeekerAndHidersInfo()

        self.seeker = Seeker(pos=seeker_pos, vissionRange=3)
        self.mapGame.addSeeker(self.seeker)
        self.hiderList = []

        for index, hider_pos in enumerate(hider_pos_list):
            hider = Hider(index ,seeker=self.seeker, pos=hider_pos, pingResetInterval=pingResetInterval, visionRange=3, map=self.mapGame)
            self.hiderList.append(hider)
            if self.level == 1:
                break
        
        while len(self.hiderList) < 3 and (self.level == 2 or self.level == 3):
            hider = Hider(len(self.hiderList) ,seeker=self.seeker, pos=self.mapGame.getRandomPos(), pingResetInterval=pingResetInterval, visionRange=3, map=self.mapGame)
            self.hiderList.append(hider)

        self.numberOfSteps = 1
        self.totalHider = len(self.hiderList)

        self.subScreen = pygame.display.set_mode((self.mapGame.colsNum*CELL_SIZE, self.mapGame.rowsNum*CELL_SIZE))
        
        print("Entering Play State")
        

    def onExit(self):
        print("Exiting Play State")

    def getStateID(self):
        return self._playID
    
    def disPlayMapGui(self, subScreen):
        grid = self.mapGame.grid
        vision_cells = self.seeker.getSight(self.mapGame)
        for cell in vision_cells:
            pygame.draw.rect(
                # Yellow with transparency
                subScreen, PINK, (cell[1] * CELL_SIZE, cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for r in range(self.mapGame.rowsNum):
            for c in range(self.mapGame.colsNum):
                rect = pygame.Rect(c * CELL_SIZE, r *
                               CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if grid[r, c] == 1:
                    subScreen.blit(self.wallPNG, rect)
                elif grid[r, c] == 2:
                    subScreen.blit(self.hiderPNG, rect)
                elif grid[r, c] == 3:
                    subScreen.blit(self.seekerPNG, rect)
                elif grid[r, c] == 9:
                    subScreen.blit(self.pingPNG, rect)
        x = 0
        y = 0

        for l in range(self.mapGame.rowsNum):
            y += CELL_SIZE
            pygame.draw.line(subScreen, BLACK, (0, y), (CELL_SIZE * self.mapGame.colsNum, y))

        for l in range(self.mapGame.colsNum):
            x += CELL_SIZE
            pygame.draw.line(subScreen, BLACK, (x, 0), (x, CELL_SIZE * self.mapGame.rowsNum))