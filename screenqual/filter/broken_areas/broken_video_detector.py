import numpy as np
import cv2
import screenqual
from screenqual.core.analyser_result import AnalyserResult
import os
from screenqual.filter.broken_areas.broken_areas_analyser import BrokenAreasAnalyser


class BrokenVideosAnalyser(BrokenAreasAnalyser):

    def __init__(self):
        super(BrokenVideosAnalyser, self).__init__()
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
        min_area = self._get_min_area(w, h)
        max_area = self._get_max_area(w, h)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if self._is_cnt_rect(approx):
                area = cv2.contourArea(approx)
                if min_area <= area <= max_area:
                    bounding_rect = self._get_rect_from_cnt(approx)
                    if self._dist(self._cut_rectangle_from_img(gray, bounding_rect)) < self.__threshold:
                        return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()
