import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class TextNearEdgeDetector(ScreenshotAnalyser):
    tolerance = 0.01
    frame_height = 2
    min_pixels_in_line_ratio = 0.01

    def execute(self, screenshot):
        img = screenshot.image
        assert img.shape[0] > 2 * self.frame_height, "Img is too narrow (height is {0} pixels)".format(img.shape[0])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = 255 - img[..., 2]
        has_text_near_horizontal_edge = self._check_horizontal_edges(img)
        has_text_near_vertical_edge   = self._check_vertical_edges(img)

        if has_text_near_horizontal_edge and has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal and vertical border crosses the text"})
        elif has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Vertical border crosses the text"})
        elif has_text_near_horizontal_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal border crosses the text"})
        else:
            return AnalyserResult.without_anomaly()

    def _check_horizontal_edges(self, img):
        row_sums = np.sum(img, axis=1)
        min_pixels_in_line = img.shape[1] * self.min_pixels_in_line_ratio
        median_row_sum = np.median(row_sums[row_sums > min_pixels_in_line])
        head = row_sums[:self.frame_height]
        tail = row_sums[-self.frame_height:]
        return max(np.max(head), np.max(tail)) > self.tolerance * median_row_sum

    def _check_vertical_edges(self, img):
        col_sums = np.sum(img, axis=0)
        min_pixels_in_col = img.shape[0] * self.min_pixels_in_line_ratio
        median_col_sum = np.median(col_sums[col_sums > min_pixels_in_col])
        head = col_sums[:self.frame_height]
        tail = col_sums[-self.frame_height:]
        return max(np.max(head), np.max(tail)) > self.tolerance * median_col_sum
