from pathlib import Path
from Map import Map
from Seeker import Seeker
from Hider import Hider
import os
from source_gui.Game import Game
import pygame



if __name__ == '__main__':
    Game.Instance().init(800, 600, "Hide & Seek")
    FPS = 60
    while Game.Instance().isRunning():
        Game.Instance().handle_event()
        Game.Instance().update()
        Game.Instance().render()

        pygame.time.Clock().tick(FPS)
    Game.Instance().clean()
