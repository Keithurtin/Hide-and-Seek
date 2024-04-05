
from GameObject import GameObject

class GameObjectFactory(object):
    def __init__(self):
        self._game_objects = []

    def getGameObjects(self, surfaceId):
        return [game_object for game_object in self._game_objects if game_object.surfaceId == surfaceId]

    def add(self, game_object : GameObject):
        self._game_objects.append(game_object)
        game_object.onEnter()

    def remove(self, game_object : GameObject):
        self._game_objects.remove(game_object)

    def clear(self):
        self._game_objects.clear()

    def update(self):
        for game_object in self._game_objects:
            game_object.update()

    def render(self):
        for game_object in self._game_objects:
            game_object.render()

    def handleEvents(self, event):
        for game_object in self._game_objects:
            game_object.handleEvents(event)