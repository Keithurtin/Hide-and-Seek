from GameObject import GameObject


class InputHandler():
    _instance = None

    @staticmethod
    def Instance():
        if InputHandler._instance is None:
            InputHandler._instance = InputHandler()
        return InputHandler._instance

    def __init__(self):
        self._input = None
