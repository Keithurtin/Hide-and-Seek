from GameState import GameState
from GameObjectFactory import GameObjectFactory
from GameStateMachine import GameStateMachine
from SurfaceManager import SurfaceManager
from ButtonObject import ButtonObject
from TextButtonObject import TextButtonObject
from GlobalInfo import GlobalInfo

import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Map import Map
from Seeker import Seeker
from Hider import Hider
import os
import pygame

GameStateMachine.gameStates["END"] = None

class EndGameState(GameState):
    def __init__(self):
        self._endID = "END"
        self.gameObjectFactory = GameObjectFactory()


    def update(self):
        self.gameObjectFactory.update()

    def render(self):
        self.gameObjectFactory.render()
        SurfaceManager.Instance().addText("YOU WIN", 40, (0, 255, 255), "youwin")
        SurfaceManager.Instance().draw("youwin", 235, 40)

        SurfaceManager.Instance().addText("score: ", 16, (255, 255, 255), "score_text")
        SurfaceManager.Instance().draw("score_text", 235, 120)

        SurfaceManager.Instance().addText(str(GlobalInfo.Instance().getGlobalInfo("score")), 16, (255, 255, 255), "point")
        SurfaceManager.Instance().draw("point", 500, 120)

        SurfaceManager.Instance().addText("Number Of Steps: ", 16, (255, 255, 255), "numberOfSteps_text")
        SurfaceManager.Instance().draw("numberOfSteps_text", 235, 170)

        SurfaceManager.Instance().addText(str(GlobalInfo.Instance().getGlobalInfo("numberOfSteps")), 16, (255, 255, 255), "numberOfSteps")
        SurfaceManager.Instance().draw("numberOfSteps", 545, 170)



    def handleEvents(self, event):
        self.gameObjectFactory.handleEvents(event)

    def onEnter(self):
        GameStateMachine.gameStates["END"] = self
        g_pathToAssets = Path(__file__).parents[2] / "asset"

        screen = pygame.display.set_mode((800, 600))

        self.gameObjectFactory.add(ButtonObject(
             fileName=f'{g_pathToAssets}/PixelGUI\PixelGUI\OptBtn.png', 
             surfaceId="play_button", 
             x=300, y=240, width=200, height=None, 
             action=lambda: GameStateMachine.Instance().changeState(GameStateMachine.gameStates["MENU"]),
             hasEffectClickDown=True, 
             fileNameEffectClickDown=f'{g_pathToAssets}\PixelGUI\PixelGUI\OptClick.png',
             ))
      
        self.gameObjectFactory.add(ButtonObject(
             fileName=f'{g_pathToAssets}\PixelGUI\PixelGUI\ExitBtn.png', 
             surfaceId="exit_button", 
             x=300, y=350, width=200, height=None, 
             action=lambda: pygame.quit(),
             hasEffectClickDown=True, 
             fileNameEffectClickDown=f'{g_pathToAssets}\PixelGUI\PixelGUI\ExitClick.png',
             ))
        print("Entering Play State")
        

    def onExit(self):
        print("Exiting Play State")

    def getStateID(self):
        return self._endID