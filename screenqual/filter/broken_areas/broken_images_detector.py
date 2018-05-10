import numpy as np
import cv2
from screenqual.core.analyser_result import AnalyserResult
from screenqual.util.rectangle import Rectangle
from screenqual.filter.broken_areas.broken_areas_analyser import BrokenAreasAnalyser

class BrokenImagesAnalyser(BrokenAreasAnalyser):

    def _check_the_same_color(self, img, bounding_rect, not_roi):
        # Choose some pixel in the center as a base colour
        base_colour = img[bounding_rect.y_upper_left + int(bounding_rect.h / 2)][
            bounding_rect.x_upper_left + int(bounding_rect.w / 2)]
        rect = self._cut_rectangle_from_img(img, bounding_rect)
        has_base_colour = np.all(rect == base_colour, axis=2)
        return np.all(np.logical_or(has_base_colour, not_roi))

    def _is_rectangular_broken_image(self, cnt, img, thresh):
        rect = self._get_rect_from_cnt(cnt)
        not_roi = self._cut_rectangle_from_img(thresh, rect) > 0
        return self._check_the_same_color(img, rect, not_roi)

    def _is_cnt_broken_images_with_round_edges(self, cnt, img, thresh):
        bounding_rect = Rectangle(*cv2.boundingRect(cnt))
        if bounding_rect.get_area() - cv2.contourArea(cnt) <= bounding_rect.get_area() * 0.1:
            not_roi = self._cut_rectangle_from_img(thresh, bounding_rect) > 0
            return self._check_the_same_color(img, bounding_rect, not_roi)
        return False

    def execute(self, screenshot):
        img = screenshot.image
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        kernel = np.ones((20, 20), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        # Cut out edges not to consider them
        kernel = np.ones((10, 10), np.uint8)
        thresh = cv2.dilate(thresh, kernel)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.INTERSECT_FULL)
        w, h = img.shape[:2]
        min_area = self._get_min_area(w, h)
        max_area = self._get_max_area(w, h)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(approx)
            if min_area <= area <= max_area:
                # A rectangular case
                if self._is_cnt_rect(approx):
                    if self._is_rectangular_broken_image(approx, img, thresh):
                        return AnalyserResult.with_anomaly()
                # Rectangular with round edges case
                if self._is_cnt_broken_images_with_round_edges(approx, img, thresh):
                    return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()
