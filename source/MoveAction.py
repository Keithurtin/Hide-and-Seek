from enum import Enum

class MoveAction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)
    STAY = (0, 0)

    @staticmethod
    def get_fromTuple(move):
        for action in MoveAction:
            if action.value == move:
                return action
        return None