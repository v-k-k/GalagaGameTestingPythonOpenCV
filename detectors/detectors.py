from enum import Enum, auto
from .base_detector import Detector
import constants


class PlayerDetector(Detector):
    _area = constants.PLAYER_AREA


class EnemyDetector(Detector):
    _area = constants.ENEMY_AREA


class MissileDetector(Detector):
    _area = constants.MISSILE_AREA


class DetectorsEnum(Enum):
    Player = auto()
    Enemy = auto()
    Missile = auto()
