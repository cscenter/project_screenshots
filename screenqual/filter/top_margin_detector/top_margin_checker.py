from screenqual.core.analyser_result import AnalyserResult

from screenqual.filter.screenshot_analyser import ScreenshotAnalyser

import numpy as np


class TopMarginChecker(ScreenshotAnalyser):

    def __init__(self, threshold=30):
        self.threshold = threshold

    def execute(self, screenshot):
        img = screenshot.image
        margin = 0
        for i in range(img.shape[0]):
            if all(np.array_equal(img[i][j], [255, 255, 255]) for j in range(img.shape[1])):
                margin += 1
            else:
                break
        if margin >= self.threshold:
            return AnalyserResult.with_anomaly({"cause": "Top margin is too large", "top margin": margin})
        return AnalyserResult.without_anomaly()
