
from pathlib import Path
from GameState import GameState
from SurfaceManager import SurfaceManager
import pygame
from GameStateMachine import GameStateMachine
from PlayGameState import PlayGameState
from InputGameState import InputGameState
from GameObjectFactory import GameObjectFactory
from InputBox import InputBox
from ButtonObject import ButtonObject
from TextButtonObject import TextButtonObject


g_pathToAssets = Path(__file__).parents[2] / "asset"

GameStateMachine.gameStates["MENU"] = None

class MenuGameState(GameState):
    def __init__(self):
        self._menuID = "MENU"
        self.gameObjectFactory = GameObjectFactory()

    def update(self):
        self.gameObjectFactory.update()


    def render(self):
        self.gameObjectFactory.render()
        SurfaceManager.Instance().addText("Hide and Seek", 40, (0, 255, 255), "hide_seek")
        SurfaceManager.Instance().draw("hide_seek", 100, 40)

        
    def handleEvents(self, event):
            self.gameObjectFactory.handleEvents(event)        

    def onEnter(self):
        GameStateMachine.gameStates["MENU"] = self

        self.gameObjectFactory.add(ButtonObject(
             fileName=f'{g_pathToAssets}/PixelGUI\PixelGUI\PlayBtn.png', 
             surfaceId="play_button", 
             x=300, y=170, width=200, height=None, 
             action=lambda: GameStateMachine.Instance().changeState(PlayGameState()),
             hasEffectClickDown=True, 
             fileNameEffectClickDown=f'{g_pathToAssets}\PixelGUI\PixelGUI\PlayClick.png',
             ))
        self.gameObjectFactory.add(ButtonObject(
             fileName=f'{g_pathToAssets}\PixelGUI\PixelGUI\ExitBtn.png', 
             surfaceId="exit_button", 
             x=300, y=270, width=200, height=None, 
             action=lambda: pygame.quit(),
             hasEffectClickDown=True, 
             fileNameEffectClickDown=f'{g_pathToAssets}\PixelGUI\PixelGUI\ExitClick.png',
             ))
        self.gameObjectFactory.add(TextButtonObject(
             inlineText="Map",
             fontSize = 80,
             fileName=f'{g_pathToAssets}\PixelGUI\PixelGUI\layer4.png', 
             surfaceId="map_label", 
             x=180, y=380, width=150, height=None, 
             action=lambda: None,
             hasEffectClickDown=False, 
             fileNameEffectClickDown=None,
             hasEffectHover=False,
             ))
        self.gameObjectFactory.add(TextButtonObject(
             inlineText="Level",
             fontSize = 60,
             fileName=f'{g_pathToAssets}\PixelGUI\PixelGUI\layer4.png', 
             surfaceId="levl_label", 
             x=180, y=450, width=150, height=None, 
             action=lambda: None,
             hasEffectClickDown=False, 
             fileNameEffectClickDown=None,
             hasEffectHover=False,
             ))
        
        self.gameObjectFactory.add(TextButtonObject(
             inlineText="Ping Reset",
             fontSize = 40,
             fileName=f'{g_pathToAssets}\PixelGUI\PixelGUI\layer4.png', 
             surfaceId="pingReset_label", 
             x=180, y=520, width=150, height=None, 
             action=lambda: None,
             hasEffectClickDown=False, 
             fileNameEffectClickDown=None,
             hasEffectHover=False,
             ))
        self.gameObjectFactory.add(InputBox( default_text="map2.txt",font_size=20, x=400, y=380, width=300, height=55, surfaceId="inputMap_box"))
        self.gameObjectFactory.add(InputBox( default_text="2", font_size=20, x=400, y=450, width=100, height=55, surfaceId="inputLevel_box"))
        self.gameObjectFactory.add(InputBox( default_text="5", font_size=20, x=400, y=520, width=100, height=55, surfaceId="inputPingReset_box"))
        
        print("Entering Menu State")
        

    def onExit(self):
        self.gameObjectFactory.clear()
        print("Exiting Menu State")

    def getStateID(self):
        return self._menuID