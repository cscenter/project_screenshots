import cv2
import numpy as np
import screenqual
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
import os


class GeneralDetector(ScreenshotAnalyser):
    def __init__(self):
        path2models = os.path.join(os.path.dirname(screenqual.__file__), "models")
        self.__avg_spectre = np.load(       os.path.join(path2models, "general_detector", "avg_spectre.npy"))
        self.__spectre_indicies = np.load(  os.path.join(path2models, "general_detector", "spectre_indices.npy"))
        self.__threshold = np.loadtxt(      os.path.join(path2models, "general_detector", "threshold.txt"))

        assert self.__avg_spectre.shape == self.__spectre_indicies.shape, "wrong model"

    def execute(self, screenshot):
        img = cv2.cvtColor(screenshot.image, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, self.__avg_spectre.shape)
        spectrum = np.fft.fft2(img)
        fshift = np.fft.fftshift(spectrum)
        magnitude_spectrum = np.log(1 + np.abs(fshift))
        spdiff = np.abs(magnitude_spectrum - self.__avg_spectre)
        spdiff[self.__spectre_indicies == 0] = 0
        sum_diff = spdiff.sum()
        # print sum_diff
        if sum_diff > self.__threshold:
            return AnalyserResult.with_anomaly({
                "spectre diff": sum_diff,
                "expected spectre diff": self.__threshold.item(0)
            })

        return AnalyserResult.without_anomaly()
