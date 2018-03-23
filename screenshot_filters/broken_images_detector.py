import numpy as np
import cv2
import math, random
from screenshot_analyser import ScreenshotAnalyser

class BrokenImagesAnalyser(ScreenshotAnalyser):

    def execute(self, screenshot):
        img = screenshot.image
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, 1)
        f, contours, h = cv2.findContours(thresh, 1, 2)
        w, h, _ = img.shape
        min_area = w * h / 200
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if (area >= min_area):
                    y_vals = [approx[0][0][1], approx[1][0][1], approx[2][0][1], approx[3][0][1]]
                    x_vals = [approx[0][0][0], approx[1][0][0], approx[2][0][0], approx[3][0][0]]
                    x_vals.sort()
                    y_vals.sort()
                    not_complete = True
                    base_colour = img[random.randint(y_vals[1] + 5, y_vals[2] - 5)][
                        random.randint(x_vals[1] + 5, x_vals[2] - 5)]
                    for i in range(y_vals[1] + 5, y_vals[2] - 5):
                        if not_complete:
                            for j in range(x_vals[1] + 5, x_vals[2] - 5):
                                if all(img[i][j] != base_colour):
                                    print (base_colour)
                                    print(img[i][j])
                                    not_complete = False
                                    break
                    if not_complete:
                        screenshot.result.append("Broken images detected")
                        return True
        return False

