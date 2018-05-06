from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
import numpy as np


class MinVariationChecker(ScreenshotAnalyser):
    def __init__(self, min_variation=2e3):
        super(MinVariationChecker, self).__init__()
        self.__min_variation = min_variation

    def execute(self, screenshot):
        img = screenshot.image
        img = np.sum(img, axis=2, dtype=np.uint32)
        variation = np.var(img)
        info = {"variation": variation}
        if variation < self.__min_variation:
            return AnalyserResult.with_anomaly(info)
        else:
            return AnalyserResult.without_anomaly(info)
