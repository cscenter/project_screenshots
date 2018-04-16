from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
import numpy as np


class MinColorsChecker(ScreenshotAnalyser):
    min_colors = 4

    def execute(self, screenshot):
        img = screenshot.image
        img = img / 10
        img = np.sum(img, axis=2).astype(np.int64)
        bins = np.bincount(img.flat)
        bins = bins[bins > img.size * 1e-5]
        info = {"found colors": bins.size}
        print(bins.size)
        return AnalyserResult.with_anomaly(info) if bins.size < self.min_colors else AnalyserResult.without_anomaly(info)
