import numpy as np
import cv2
import math, random
from screenshot_analyser import ScreenshotAnalyser

class BrokenImagesAnalyser(ScreenshotAnalyser):

    def execute(self, screenshot):
        img = screenshot.image
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        f, contours, h = cv2.findContours(thresh, 1, 2)
        w, h, _ = img.shape
        min_area = w * h / 200
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if (area >= min_area):
                    y_vals = approx[:, 0, 1]
                    x_vals = approx[:, 0, 0]
                    x_vals.sort()
                    y_vals.sort()
                    base_colour = img[random.randint(y_vals[1] + 5, y_vals[2] - 5)][
                        random.randint(x_vals[1] + 5, x_vals[2] - 5)]
                    rect = img[y_vals[1] + 5:y_vals[2] - 5, x_vals[1] + 5:x_vals[2] - 5]
                    colour_arr = np.full(rect.shape, base_colour)
                    if (np.all(np.all(rect == colour_arr))):
                        screenshot.result.append("Broken images detected")
                        return True
        return False

