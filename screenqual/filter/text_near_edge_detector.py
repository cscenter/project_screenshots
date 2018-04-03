import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class TextNearEdgeDetector(ScreenshotAnalyser):
    tolerance = 0.1
    frame_height = 5
    min_pixels_in_line_ratio = 0.01

    def execute(self, screenshot):
        img = screenshot.image
        assert img.shape[0] > 2 * self.frame_height, "Img is too narrow (height is {0} pixels)".format(img.shape[0])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = 255 - img[..., 2]
        # check top and bottom
        row_sums = np.sum(img, axis=1)
        min_pixels_in_line = img.shape[1] * self.min_pixels_in_line_ratio
        median_row_sum = np.median(row_sums[row_sums > min_pixels_in_line])
        head = row_sums[:self.frame_height]
        tail = row_sums[-self.frame_height:]
        has_text_near_edge = max(np.max(head), np.max(tail)) > self.tolerance * median_row_sum
        if has_text_near_edge:
            return AnalyserResult(True, self.__class__.__name__, "Horizontal border crosses the text")
        else:
            return AnalyserResult(False, self.__class__.__name__)
