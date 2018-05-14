import functools
import cv2
import numpy as np

from screenqual.core.analyser_result import AnalyserResult
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser


def _find_strokes(column, eps):
    thresholded = np.concatenate(([False], column > eps, [False])).astype(int)
    starts = np.where((thresholded[1:] - thresholded[:-1]) > 0)[0]
    ends = np.where((thresholded[1:] - thresholded[:-1]) < 0)[0]

    strokes = zip(ends - starts, starts, ends)
    return strokes


def _find_max_stroke(column, eps):
    assert len(column.shape) == 1

    strokes = _find_strokes(column, eps)
    if not strokes:
        return None

    sort_stroke = sorted(strokes, reverse=True)

    min_size_img = 50
    eps = 10
    mean_stroke = min(np.percentile(sort_stroke, 50), min_size_img) + eps

    for i, item in enumerate(sort_stroke):
        if item[0] < mean_stroke:
            return sort_stroke[:i]

    return sort_stroke


def check_red_stoke(frame, max_red_pxl):
    line_sums_0 = np.sum(frame, axis=1)
    max_stoke = _find_strokes(line_sums_0, 0)
    for _, start, end in max_stoke:
        if sum(line_sums_0[start:end]) > max_red_pxl:
            return True
    return False


class RedTextDetector(ScreenshotAnalyser):
    def __init__(self):
        self.__max_red_pxl = 250
        self.__eps_red_color = 100
        self.__img_max_intensity = 255
        self.__threshold = 240

    def execute(self, screenshot):
        img = screenshot.image
        red_image = img[:, :, :2].sum(axis=2).astype(int)
        red_image = red_image + 255 - img[:, :, 2]
        red_image = red_image < self.__eps_red_color

        img_brightness = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)[:, :, 2]
        img_brightness[img_brightness > self.__threshold] = self.__img_max_intensity
        img_brightness = self.__img_max_intensity - img_brightness
        is_red_text = self._find_red_stroke(img_brightness, red_image)

        if is_red_text:
            return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()

    def _find_red_stroke(self, img_brightness, img_red):
        line_sums = np.sum(img_brightness, axis=1)
        strokes = _find_max_stroke(line_sums, 0)
        w_img = img_brightness.shape[1]

        list_img = []
        for stroke in strokes:
            line_sums_0 = np.sum(img_brightness[stroke[1]:stroke[2], :], axis=0)
            max_stoke = _find_max_stroke(line_sums_0, 0)
            if max_stoke:
                list_img.append(functools.reduce(
                    lambda x, y: y if x[1] > y[1] else x, max_stoke, max_stoke[0]))
            else:
                list_img.append([0, w_img])

        for h, w in zip(strokes, list_img):
            try:
                line_sums_1 = np.sum(img_brightness[h[1]:h[2], w[1]:w[2]], axis=1)
            except Exception:
                print(h, w)
                print(img_brightness.shape)

            for stroke in _find_max_stroke(line_sums_1, 0):
                img_red[h[1]+stroke[1]:h[1]+stroke[2], w[1]:w[2]] = 0

            if check_red_stoke(img_red[h[1]:h[2], w[1]:w[2]], self.__max_red_pxl):
                return True

            img_red[h[1]:h[2], :] = 0

        return check_red_stoke(img_red, self.__max_red_pxl)
