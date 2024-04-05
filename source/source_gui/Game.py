import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from GameStateMachine import GameStateMachine
from MenuGameState import MenuGameState
from PlayGameState import PlayGameState
from SurfaceManager import SurfaceManager
from EndGameState import EndGameState


g_pathToAssets = Path(__file__).parents[2] / "asset"
print(g_pathToAssets)

class Game():
    _instance = None

    @staticmethod
    def Instance():
        if Game._instance is None:
            Game._instance = Game()
        return Game._instance
    
    def __init__(self):
        self.running = False
        self.width = None
        self.height = None
        self.screen = None
        self.clock = None
        self.player_pos = None

    def init(self, width=800, height=600, title="Hide & Seek"):
        self.width = width
        self.height = height
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(str(g_pathToAssets) + "/human.png"))
        
        successes, failures = pygame.init()
        if failures != 0: 
            return False
        
        self.screen = pygame.display.set_mode((self.width, self.height), flags=pygame.SHOWN)
        SurfaceManager.Instance().screen = self.screen
        self.clock = pygame.time.Clock()
        # self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)

        # innit other stuff here
        GameStateMachine.Instance().pushState(MenuGameState())

        self.running = True
        return True


    def render(self):
        self.screen.fill((0, 0, 0)) # clear screen
        # screen_size = (self.width, self.height)
        SurfaceManager.Instance().addImage(str(g_pathToAssets) + "/menubackground.png", "background")

        SurfaceManager.Instance().draw("background", 0, 0, None, self.height)

        GameStateMachine.Instance().render()

    
        pygame.display.flip() # update screen

    def update(self):
        GameStateMachine.Instance().update()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            GameStateMachine.Instance().handleEvents(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.quit()
            exit()


    def isRunning(self):
        return self.running

    def quit(self):
        self.running = False

    def clean(self):
        pygame.quit()

    def getScreen(self):
        return self.screen


