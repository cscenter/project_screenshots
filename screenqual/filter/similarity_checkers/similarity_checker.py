from abc import ABCMeta, abstractmethod
import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


def _generate_spectrum(img_bgr, shape_cols_first):
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, shape_cols_first)
    spectrum = np.fft.fft2(img)
    fshift = np.fft.fftshift(spectrum)
    magnitude_spectrum = np.log(1 + np.abs(fshift))
    return magnitude_spectrum


class SimilarityChecker(ScreenshotAnalyser):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _avg_spectrum(self):
        pass

    @abstractmethod
    def _spectrum_indices(self):
        pass

    @abstractmethod
    def _threshold(self):
        pass

    def execute(self, screenshot):
        avg_spectrum = self._avg_spectrum()
        spectrum_indices = self._spectrum_indices()
        threshold = self._threshold()

        magnitude_spectrum = _generate_spectrum(screenshot.image, avg_spectrum.shape[::-1])
        spdiff = np.abs(magnitude_spectrum - avg_spectrum)
        spdiff[spectrum_indices == 0] = 0
        sum_diff = spdiff.sum()

        if sum_diff > threshold:
            return AnalyserResult.with_anomaly({
                "spectre diff": sum_diff,
                "expected spectre diff": threshold
            })

        return AnalyserResult.without_anomaly()
