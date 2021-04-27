from .detectors import DetectorsEnum, PlayerDetector, EnemyDetector, MissileDetector


class DetectorFactory:

    @staticmethod
    def create_detector(detector_type: DetectorsEnum):
        if detector_type == DetectorsEnum.Player:
            return PlayerDetector()
        if detector_type == DetectorsEnum.Enemy:
            return EnemyDetector()
        if detector_type == DetectorsEnum.Missile:
            return MissileDetector()

