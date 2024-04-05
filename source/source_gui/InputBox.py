from GameObject import GameObject
import pygame
from pathlib import Path
from SurfaceManager import SurfaceManager
from GlobalInfo import GlobalInfo

pathToAssets = Path(__file__).parents[2] / "asset"

class InputBox(GameObject):

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)

    def __init__(self, default_text, font_size, x, y, width, height, surfaceId:str):
        self.font_size = font_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surfaceId = surfaceId
        self.text = default_text
        self.active = False
        self.color_inactive = None
        self.color_active = None

        self.input_box_rect = None
        self.box_surface = None
        self.color = None
        self.font = None
        self.text_surface = None


    def update(self):
        pygame.draw.rect(self.box_surface, self.color, self.input_box_rect, 2)

        SurfaceManager.Instance().addTextBoxToSurface(self.text, self.font_size, self.color, self.surfaceId, self.input_box_rect.x + 10, self.input_box_rect.y + 15)

    def render(self):
        SurfaceManager.Instance().draw(self.surfaceId, self.x, self.y, self.width, self.height)

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if SurfaceManager.Instance().getDestRect(self.surfaceId).collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
                
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    SurfaceManager.Instance().addTextBoxToSurface(self.text, self.font_size, self.color, self.surfaceId, self.input_box_rect.x + 10, self.input_box_rect.y + 15)
        
        GlobalInfo.Instance().setGlobalInfo(self.surfaceId, self.text)

        
    def onEnter(self):
        self.color_inactive = InputBox.GRAY
        self.color_active = InputBox.BLACK

        self.input_box_rect = pygame.Rect(0, 0, self.width, self.height)
        
        self.color = self.color_inactive
        self.font = pygame.font.Font(f'{pathToAssets}\QuinqueFive_Font_1_1\QuinqueFive.ttf', self.font_size)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.box_surface = SurfaceManager.Instance().addRect((255,255,255,0), self.width, self.height, self.surfaceId)
        
        

    def onExit(self):
        pass

    def getStateID(self):
        pass