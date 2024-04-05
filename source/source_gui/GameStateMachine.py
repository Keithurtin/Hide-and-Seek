from GameState import GameState

class GameStateMachine:
    _instance = None

    gameStates = {}

    @staticmethod
    def Instance():
        if GameStateMachine._instance is None:
            GameStateMachine._instance = GameStateMachine()
        return GameStateMachine._instance

    def __init__(self):
        self._gameStates = []
        # self._currentState = None

    def pushState(self, gameState : GameState):
        self._gameStates.append(gameState)
        self._gameStates[-1].onEnter()

    def changeState(self, gameState : GameState):
        if not len(self._gameStates) == 0:
            if self._gameStates[-1].getStateID() == gameState.getStateID():
                return # do nothing
            
            if self._gameStates[-1].onExit():
                self._gameStates.pop()
        
        self._gameStates.append(gameState) 
        self._gameStates[-1].onEnter()

    def popState(self):
        if not len(self._gameStates) == 0:
            if self._gameStates[-1].onExit():
                self._gameStates.pop()
        
    def update(self):
        if not len(self._gameStates) == 0:
            self._gameStates[-1].update()
    
    def render(self):
        if not len(self._gameStates) == 0:
            self._gameStates[-1].render()

    def handleEvents(self, event):
        if not len(self._gameStates) == 0:
            self._gameStates[-1].handleEvents(event)

    def clean(self):
        while not len(self._gameStates) == 0:
            self._gameStates[-1].onExit()
            self._gameStates.pop()
            self._gameStates.clear()