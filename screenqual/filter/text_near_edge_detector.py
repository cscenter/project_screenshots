import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class TextNearEdgeDetector(ScreenshotAnalyser):
    tolerance = 0.2
    frame_height = 10
    line_eps = 10

    def execute(self, screenshot):
        img = screenshot.image
        assert min(*img.shape[:2]) > 2 * self.frame_height, "Img is too narrow (size is {0} pixels)".format(img.shape)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_max_intensity = np.percentile(img, 99)
        img = img_max_intensity - img[..., 2]
        decay_mask = self._exp_decay(img.shape)
        decayed_img = np.multiply(img, decay_mask)
        has_text_near_horizontal_edge = self._check_edges(img, decayed_img, work_axis=1)
        has_text_near_vertical_edge   = self._check_edges(img, decayed_img, work_axis=0)

        if has_text_near_horizontal_edge and has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal and vertical border crosses the text"})
        elif has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Vertical border crosses the text"})
        elif has_text_near_horizontal_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal border crosses the text"})
        else:
            return AnalyserResult.without_anomaly()

    @staticmethod
    def _exp_decay(shape):
        assert len(shape) == 2, "Only 2-dimensional mat is supported"
        edges_matrix = np.ones(shape, np.uint8)
        edges_matrix[[0, -1], :] = 0
        edges_matrix[:, [0, -1]] = 0
        distance_transform = cv2.distanceTransform(edges_matrix, cv2.DIST_L1, cv2.DIST_MASK_3)
        return 1 / np.exp(np.minimum(distance_transform.astype(np.float32), 30.))

    def _check_edges(self, original_img, decayed_img, work_axis):
        assert len(original_img.shape) == 2 and len(decayed_img.shape) == 2

        line_sums = np.sum(original_img, axis=work_axis)
        min_pixels_in_line = np.percentile(line_sums, 5)
        median_line_sum = np.median(line_sums[line_sums > min_pixels_in_line + self.line_eps])
        decayed_line_sums = np.sum(decayed_img, axis=work_axis)
        head = decayed_line_sums[:self.frame_height]
        tail = decayed_line_sums[-self.frame_height:]

        return max(np.max(head), np.max(tail)) > self.tolerance * median_line_sum
