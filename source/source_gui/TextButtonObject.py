
from GameObject import GameObject
from SurfaceManager import SurfaceManager
import pygame

class TextButtonObject(GameObject):
    def __init__(self, inlineText, fontSize, fileName, surfaceId, x, y, width, height, action=lambda: None, hasEffectClickDown=False, fileNameEffectClickDown=None, hasEffectHover=True):
        self.inlineText = inlineText
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.surfaceId = surfaceId
        self.fileName = fileName
        self.hasEffectClickDown = hasEffectClickDown
        self.fileNameEffectClickDown = fileNameEffectClickDown
        self.hasEffectHover = hasEffectHover
        self.fontSize = fontSize

    def update(self):
        pass
    
    def render(self):
        SurfaceManager.Instance().draw(self.surfaceId, self.x, self.y, self.width, self.height)
        if self.hasEffectHover:
            SurfaceManager.Instance().addHoverEffect(self.surfaceId)
        

    def handleEvents(self, event):
        if not self.hasEffectHover:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.hasEffectClickDown and SurfaceManager.Instance().getDestRect(self.surfaceId).collidepoint(x, y):
                SurfaceManager.Instance().addImage(self.fileNameEffectClickDown, self.surfaceId)

        if event.type == pygame.MOUSEBUTTONUP:
            SurfaceManager.Instance().addImage(self.fileName, self.surfaceId)
            x, y = pygame.mouse.get_pos()
            if SurfaceManager.Instance().getDestRect(self.surfaceId).collidepoint(x, y):
                self.action()

    def onEnter(self):
        SurfaceManager.Instance().addImage(self.fileName, self.surfaceId)
        SurfaceManager.Instance().addTextToSurface(self.inlineText, self.fontSize, (255, 255, 255), self.surfaceId)

    def onExit(self):
        pass

    def getStateID(self):
        pass