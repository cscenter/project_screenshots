from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class MinSizeChecker(ScreenshotAnalyser):
    min_size = 50

    def execute(self, screenshot):
        img = screenshot.image
        if img is None:
            return AnalyserResult.with_anomaly({"cause": "image is empty"})
        if len(img.shape) == 1:
            return AnalyserResult.with_anomaly({"cause": "image is 1D array"})
        if img.shape[0] < self.min_size:
            return AnalyserResult.with_anomaly({"cause": "image height is too small"})
        if img.shape[1] < self.min_size:
            return AnalyserResult.with_anomaly({"cause": "image width is too small"})

        return AnalyserResult.without_anomaly()
