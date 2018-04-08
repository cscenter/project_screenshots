import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


# seeks the maximum consecutive range of values, that are greater than eps
def find_max_stroke(column, eps):
    assert len(column.shape) == 1

    fl = column.flat
    # finds all consecutive ranges of values, that are greater than eps using the efficient numpy iterators
    islands = []
    while fl.index < column.size:
        coord = fl.coords[0]
        if fl.next() > eps:
            length = 1
            while fl.index < column.size - 1 and fl.next() > eps:
                length += 1
            # writes the length of the range, start and end coordinates
            islands.append([length, coord, coord + length])

    if not islands:
        return None

    # extracts the maximum range
    max_stroke = sorted(islands, reverse=True)[0]

    return None if max_stroke[0] < column.size / 3 else max_stroke[1:]


def exp_decay(shape):
    assert len(shape) == 2, "Only 2-dimensional mat is supported"
    edges_matrix = np.ones(shape, np.uint8)
    edges_matrix[[0, -1], :] = 0
    edges_matrix[:, [0, -1]] = 0
    distance_transform = cv2.distanceTransform(edges_matrix, cv2.DIST_L1, cv2.DIST_MASK_3)
    return 1 / np.exp(np.minimum(distance_transform.astype(np.float32), 30.))


class TextNearEdgeDetector(ScreenshotAnalyser):
    tolerance = 0.2
    frame_height = 10
    line_eps = 10
    min_pixels_in_line_ratio = 0.01

    def execute(self, screenshot):
        img = screenshot.image
        assert img.shape[0] > 2 * self.frame_height, "Img is too narrow (height is {0} pixels)".format(img.shape[0])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_max_intensity = np.percentile(img, 99)
        img = img_max_intensity - img[..., 2]
        decay_mask = exp_decay(img.shape)
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
        stroke = find_max_stroke(line_sums, min_pixels_in_line)
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
