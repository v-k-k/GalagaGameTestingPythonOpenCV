import numpy as np
import pytesseract
import cv2
import constants
from detectors import DetectorFactory, DetectorsEnum
from utils import Base, Image, Colors, Keypoints, array_to_tuple, Coordinates


class ImageControl(Base):
    keypoints = None
    __image_cache = {}
    __fighter_movements = set()

    def __init__(self, canvas_image):
        self.__canvas_image = canvas_image

    @property
    def text_content(self):
        self.logger.debug("Reading the text on canvas")
        return pytesseract.image_to_string(self.data.original).lower()

    @property
    def data(self):
        image, gray_image = self.__canvas_image()
        hashable = array_to_tuple(image)
        if hashable not in self.__image_cache:
            binary_image = cv2.Laplacian(gray_image[0:240, 0:205], cv2.CV_8UC1)
            dilated_image = cv2.dilate(binary_image, np.ones((6, 6)))
            _, thresh = cv2.threshold(dilated_image, constants.BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
            components = cv2.connectedComponentsWithStats(thresh, constants.CONNECTIVITY, cv2.CV_32S)
            centers = components[3]
            retval, threshold = cv2.threshold(thresh, 200, 255, cv2.THRESH_BINARY_INV)
            self.__image_cache[hashable] = threshold
            return Image(image, threshold)
        return Image(image, self.__image_cache[hashable])

    def load_keypoints(self):
        threshold = self.data.threshold
        self.keypoints = Keypoints(DetectorFactory.create_detector(DetectorsEnum.Player)
                                                  .detect(threshold),
                                   DetectorFactory.create_detector(DetectorsEnum.Enemy)
                                                  .detect(threshold),
                                   DetectorFactory.create_detector(DetectorsEnum.Missile)
                                                  .detect(threshold))
        if bool(self.keypoints.player):
            self.__fighter_movements.add(Coordinates(self.keypoints.player[-1].pt[1], self.keypoints.player[-1].pt[0]))

    def draw_keypoints(self):
        image = self.data.original
        for keypoint in self.keypoints:
            if keypoint == self.keypoints.player:
                point_color = Colors.GREEN.value
            elif keypoint == self.keypoints.enemy:
                point_color = Colors.RED.value
            else:
                point_color = Colors.BLACK.value
            image = cv2.drawKeypoints(
                image, keypoint, np.array([]), point_color,
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
        return image

    def is_initial_screen_visible(self):
        content = self.text_content
        return "1981" in content or "1985" in content

    def is_missile_launched(self):
        return self.keypoints.missile

    def is_fighter_moved(self):
        self.logger.critical(self.__fighter_movements)
        return len(self.__fighter_movements) >= 2
