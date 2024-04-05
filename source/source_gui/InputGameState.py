from GameState import GameState

class InputGameState(GameState):
    def __init__(self):
        self._inputID = "Input"

    def update(self):
        pass

    def render(self):
        pass

    def handleEvents(self, event):
        pass

    def onEnter(self):
        print("Entering Input State")

    def onExit(self):
        print("Exiting Input State")

    def getStateID(self):
        return self._inputID