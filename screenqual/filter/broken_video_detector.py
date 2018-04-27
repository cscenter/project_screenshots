import numpy as np
import cv2
import screenqual
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
from screenqual.util.rectangle import Rectangle
import os
import math


class BrokenVideosAnalyser(ScreenshotAnalyser):

    def __init__(self):
        path2models = os.path.join(os.path.dirname(screenqual.__file__), "models")
        self.__mean_hist = np.load(os.path.join(path2models, "broken_videos", "model.npy"))
        self.__threshold = np.loadtxt(os.path.join(path2models, "broken_videos", "threshold.txt"))

    def _dist(self, img):
        img = cv2.resize(img, (159, 86))
        num_of_bins = 26
        hist = cv2.calcHist([img], [0], None, [num_of_bins], [0, 256])
        return np.sqrt(np.sum((hist - self.__mean_hist) ** 2))

    def execute(self, screenshot):
        img = screenshot.image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.INTERSECT_FULL)
        w, h = img.shape[:2]
        min_area = w * h * 0.002
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if area >= min_area:
                    x_vals = approx[:, 0, 0]
                    y_vals = approx[:, 0, 1]
                    bounding_rect = Rectangle(x=x_vals.min() + 5, y=y_vals.min() + 5,
                                              w=x_vals.max() - x_vals.min() - 10,
                                              h=y_vals.max() - y_vals.min() - 10)
                    if self._dist(gray[bounding_rect.y_upper_left:bounding_rect.y_bottom_right,
                                  bounding_rect.x_upper_left:bounding_rect.x_bottom_right]) < \
                            self.__threshold:
                        return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()
