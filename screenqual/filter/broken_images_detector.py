import numpy as np
import cv2
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class BrokenImagesAnalyser(ScreenshotAnalyser):

    def __check_the_same_color(self, img, x, y, h, w, not_roi):
        # Choose some pixel in the center as a base colour
        base_colour = img[y + int(h / 2)][x + int(w / 2)]
        rect = img[y:y + h, x :x + w]
        colour_arr = np.full(rect.shape, base_colour)
        check_arr = np.all(rect == colour_arr, axis = 2)
        if np.all(np.logical_or(check_arr, not_roi)):
            return True
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
        f, contours, h = cv2.findContours(thresh, 1, 2)
        w, h, _ = img.shape
        min_area = w * h * 0.002
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            # A rectangular case
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if area >= min_area:
                    x_vals = approx[:, 0, 0]
                    y_vals = approx[:, 0, 1]
                    x_vals.sort()
                    y_vals.sort()
                    h = y_vals[2] - y_vals[1]
                    w = x_vals[2] - x_vals[1]
                    x_val = x_vals[1]
                    y_val = y_vals[1]
                    not_roi = thresh[y_val:y_val+h, x_val:x_val + w] > 0
                    if self.__check_the_same_color(
                            img, x_val, y_val, h, w, not_roi):
                        cv2.drawContours(img, [cnt], 0, (0, 255, 0), 3)
                        cv2.imwrite("th.png", img)
                        return AnalyserResult.with_anomaly()
            x_bound, y_bound, w_bound, h_bound = cv2.boundingRect(approx)
            area_bound = w_bound * h_bound
            area_cnt = cv2.contourArea(approx)
            # Rectangular with round edges case
            if area_bound - area_cnt <= area_bound * 0.1:
                not_roi = thresh[y_bound:y_bound + h_bound, x_bound:x_bound + w_bound] > 0
                # Take some pixel in center to make sure that it is not
                # pixel on round edge
                if self.__check_the_same_color(
                        img, x_bound, y_bound, h_bound, w_bound, not_roi):
                    cv2.drawContours(img, [approx], 0, (0, 255, 0), 3)
                    cv2.imwrite("th.png", thresh)
                    return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()
