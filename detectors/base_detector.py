import constants
import cv2


class Detector:
    _params = cv2.SimpleBlobDetector_Params()
    _filters = constants.FILTERS
    _area = None
    _detector = None
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(Detector, cls).__new__(cls)
        return cls.__instance

    def _add_filters(self):
        self._params.filterByArea, self._params.filterByCircularity, \
            self._params.filterByConvexity, self._params.filterByInertia = self._filters
        self._params.minArea, self._params.maxArea = self._area

    def create_object(self):
        if self._detector is None:
            self._add_filters()
            self._detector = cv2.SimpleBlobDetector_create(self._params)
        return self._detector

    def detect(self, *args, **kwargs):
        if self._detector is None:
            self.create_object()
        return self._detector.detect(*args, **kwargs)