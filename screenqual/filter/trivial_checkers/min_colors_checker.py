from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
import numpy as np


class MinColorsChecker(ScreenshotAnalyser):
    def __init__(self, min_colors=4):
        super(MinColorsChecker, self).__init__()
        self.__min_colors = min_colors

    def execute(self, screenshot):
        img = screenshot.image
        img = img / 10
        img = np.sum(img, axis=2).astype(np.int64)
        bins = np.bincount(img.flat)
        bins = bins[bins > img.size * 1e-5]
        info = {"found colors": bins.size}
        return AnalyserResult.with_anomaly(info) if bins.size < self.__min_colors else AnalyserResult.without_anomaly(info)
