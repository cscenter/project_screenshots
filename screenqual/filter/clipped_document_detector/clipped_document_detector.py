import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


def _find_strokes(column, eps):
    thresholded = np.concatenate(([False], column > eps, [False])).astype(int)
    starts = np.where((thresholded[1:] - thresholded[:-1]) > 0)[0]
    ends   = np.where((thresholded[1:] - thresholded[:-1]) < 0)[0]

    strokes = zip(ends - starts, starts, ends)
    return strokes


def _find_max_stroke(column, eps):
    assert len(column.shape) == 1

    strokes = _find_strokes(column, eps)

    if not strokes:
        return None

    max_stroke = sorted(strokes, reverse=True)[0]

    return None if max_stroke[0] < column.size / 3 else max_stroke[1:]


def _exp_decay(shape):
    assert len(shape) == 2, "Only 2-dimensional mat is supported"
    edges_matrix = np.ones(shape, np.uint8)
    edges_matrix[[0, -1], :] = 0
    edges_matrix[:, [0, -1]] = 0
    distance_transform = cv2.distanceTransform(edges_matrix, cv2.DIST_L1, cv2.DIST_MASK_3)
    return 1 / np.exp(np.minimum(distance_transform.astype(np.float32), 30.))


class ClippedDocumentDetector(ScreenshotAnalyser):
    tolerance = 0.2
    frame_height = 10
    line_eps = 10
    min_pixels_in_line_ratio = 0.01

    def execute(self, screenshot):
        img = screenshot.image
        assert img.shape[0] > 2 * self.frame_height, "Img is too narrow (height is {0} pixels)".format(img.shape[0])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[..., 2]
        img_max_intensity = np.percentile(img, 99)
        img = img_max_intensity - img
        decay_mask = _exp_decay(img.shape)
        decayed_img = np.multiply(img, decay_mask)
        has_text_near_horizontal_edge = self._check_horizontal_edges(img, decayed_img)
        has_text_near_vertical_edge   = self._check_vertical_edges(img, decayed_img)

        if has_text_near_horizontal_edge and has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal and vertical border crosses the text"})
        if has_text_near_vertical_edge:
            return AnalyserResult.with_anomaly({"cause": "Vertical border crosses the text"})
        if has_text_near_horizontal_edge:
            return AnalyserResult.with_anomaly({"cause": "Horizontal border crosses the text"})
        return AnalyserResult.without_anomaly()

    def _check_vertical_edges(self, original_img, decayed_img):
        assert len(original_img.shape) == 2 and len(decayed_img.shape) == 2

        line_sums = np.sum(original_img, axis=1)
        min_pixels_in_line = np.percentile(line_sums, 5)
        stroke = _find_max_stroke(line_sums, min_pixels_in_line)
        if stroke:
            min_y, max_y = stroke
            original_img = original_img.copy()
            decayed_img = decayed_img.copy()
            original_img[min_y:max_y, :] = 0
            decayed_img[min_y:max_y, :] = 0

        return self._check_edges(original_img, decayed_img, 0)

    def _check_horizontal_edges(self, original_img, decayed_img):
        return self._check_edges(original_img, decayed_img, 1)

    def _check_edges(self, original_img, decayed_img, work_axis):
        assert len(original_img.shape) == 2 and len(decayed_img.shape) == 2

        line_sums = np.sum(original_img, axis=work_axis)
        min_pixels_in_line = np.percentile(line_sums, 5)
        target_line_sums = line_sums[line_sums > min_pixels_in_line + self.line_eps]
        if not target_line_sums.size:
            return False
        median_line_sum = np.median(target_line_sums)
        decayed_line_sums = np.sum(decayed_img, axis=work_axis)
        head = decayed_line_sums[:self.frame_height]
        tail = decayed_line_sums[-self.frame_height:]
        return max(np.max(head), np.max(tail)) > self.tolerance * median_line_sum
