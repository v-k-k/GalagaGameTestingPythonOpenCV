from enum import Enum
import constants


class Timeouts(Enum):
    MIN = 0.01
    MID = 0.1 if constants.DEBUG_MODE else 0.5
    MAX = 1 if constants.DEBUG_MODE else 3
