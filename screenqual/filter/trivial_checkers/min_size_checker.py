from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class MinSizeChecker(ScreenshotAnalyser):
    def __init__(self, min_size=(50, 50)):
        """
        :param min_size: expected rows number is at the first position, expected cols number is at the second one
        """
        super(MinSizeChecker, self).__init__()
        self.__min_size = min_size

    def execute(self, screenshot):
        img = screenshot.image
        if img is None:
            return AnalyserResult.with_anomaly({"cause": "image is empty"})
        if len(img.shape) == 1:
            return AnalyserResult.with_anomaly({"cause": "image is 1D array"})
        if img.shape[0] < self.__min_size[0]:
            return AnalyserResult.with_anomaly({"cause": "image height is too small"})
        if img.shape[1] < self.__min_size[1]:
            return AnalyserResult.with_anomaly({"cause": "image width is too small"})

        return AnalyserResult.without_anomaly()
