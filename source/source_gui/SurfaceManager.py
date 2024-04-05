import pygame
from pathlib import Path

pathToAssets = Path(__file__).parents[2] / "asset"

class SurfaceManager():
    _instance = None
    screen = None

    @staticmethod
    def Instance():
        if SurfaceManager._instance is None:
            SurfaceManager._instance = SurfaceManager()
        return SurfaceManager._instance

    def __init__(self):
        self.surfaces = {}
        self.destRects = {}

    def addRect(self, color : tuple, width : int, height : int, surfaceId : str):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        self.surfaces[surfaceId] = surface
        return surface
    
    def updateSurface(self, surfaceId, Surface):
        self.surfaces[surfaceId] = Surface

    def addText2Rect(self, text : str, font, size : int, color : tuple, width : int, height : int, surfaceId : str):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_width, text_height = text_surface.get_size()

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        surface = pygame.Surface((width, height))
        surface.fill((255, 255, 255))
        surface.blit(text_surface, (x, y))

        self.surfaces[surfaceId] = surface


    def addImage(self, fileName : str, surfaceId : str):
        image_surface = pygame.image.load(fileName)
        image_surface.convert()

        self.surfaces[surfaceId] = image_surface

    def addText(self, text : str, font, size : int, color : tuple, surfaceId : str):
        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)
        self.surfaces[surfaceId] = text_surface

    def addText(self, text : str, size : int, color : tuple, surfaceId : str):
        font = pygame.font.Font(f'{pathToAssets}\QuinqueFive_Font_1_1\QuinqueFive.ttf', size)
        text_surface = font.render(text, True, color)
        self.surfaces[surfaceId] = text_surface

    def addTextBoxToSurface(self, text: str, size: int, color: tuple, surfaceId: str, x:int, y:int):
        if surfaceId not in self.surfaces:
            return
        font = pygame.font.Font(f'{pathToAssets}\QuinqueFive_Font_1_1\QuinqueFive.ttf', size)
        text_surface = font.render(text, True, color)
        self.surfaces[surfaceId].fill((255, 255, 255, 0))
        surface_width, surface_height = self.surfaces[surfaceId].get_size()
        text_width, text_height = text_surface.get_size()

        if x is None and y is None:
            x = (surface_width - text_width) // 2
            y = (surface_height - text_height) // 2 - 30

        self.surfaces[surfaceId].blit(text_surface, (x, y))

    def addTextToSurface(self, text: str, size: int, color: tuple, surfaceId: str):
        if surfaceId not in self.surfaces:
            return
        font = pygame.font.Font(f'{pathToAssets}\QuinqueFive_Font_1_1\QuinqueFive.ttf', size)
        text_surface = font.render(text, True, color)
        surface_width, surface_height = self.surfaces[surfaceId].get_size()
        text_width, text_height = text_surface.get_size()

        x = (surface_width - text_width) // 2
        y = (surface_height - text_height) // 2 - 30

        self.surfaces[surfaceId].blit(text_surface, (x, y))
        



    def draw(self, surfaceId : str, x, y, width = None, height = None):
        surface = self.surfaces[surfaceId]
        width_surface = surface.get_width()
        height_surface = surface.get_height()

        if width is None and height is not None:
            width = width_surface / height_surface * height
        if height is None and width is not None:
            height = height_surface / width_surface * width
        if width is None and height is None:
            width = width_surface
            height = height_surface
        
        self.destRects[surfaceId] = (x, y, width, height)

        surface = pygame.transform.scale(surface, (width, height))
        if surface is not None:
            self.screen.blit(surface, (x, y, width, height))
        else:
            print(f"Surface {surfaceId} not found")

    def getDestRect(self, surfaceId):
        return pygame.Rect(self.destRects[surfaceId])

    def addHoverEffect(self, surfaceId):
        surface = self.surfaces[surfaceId]
        surface = pygame.transform.scale(surface, (self.destRects[surfaceId][2], self.destRects[surfaceId][3]))
        hover_surface = surface.copy()
        hover_surface.convert_alpha()
        brighten = 25
        hover_surface.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
        x, y = pygame.mouse.get_pos()
        if pygame.Rect(self.getDestRect(surfaceId)).collidepoint(x, y):
            self.screen.blit(hover_surface, self.getDestRect(surfaceId))
        else:
            self.screen.blit(surface, self.getDestRect(surfaceId))
        
    
    
    def clear(self):
        self.surfaces.clear()
    

