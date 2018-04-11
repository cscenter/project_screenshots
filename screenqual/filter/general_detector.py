import cv2
import numpy as np
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
import os


class GeneralDetector(ScreenshotAnalyser):
    def __init__(self):
        ScreenshotAnalyser.__init__(self)
        self.avg_spectre = np.load(os.path.join(self.path2models,       "general_detector", "avg_spectre.npy"))
        self.spectre_indicies = np.load(os.path.join(self.path2models,  "general_detector", "spectre_indices.npy"))
        self.threshold = np.loadtxt(os.path.join(self.path2models,      "general_detector", "threshold.txt"))

        assert self.avg_spectre.shape == self.spectre_indicies.shape, "wrong model"

    def execute(self, screenshot):
        img = cv2.cvtColor(screenshot.image, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, self.avg_spectre.shape)
        spectrum = np.fft.fft2(img)
        fshift = np.fft.fftshift(spectrum)
        magnitude_spectrum = np.log(np.abs(fshift))
        spdiff = np.abs(magnitude_spectrum - self.avg_spectre)
        spdiff[self.spectre_indicies == 0] = 0
        sum_diff = spdiff.sum()
        return AnalyserResult.with_anomaly({"spectre diff": sum_diff, "expected spectre diff": self.threshold}) \
            if sum_diff > self.threshold else AnalyserResult.without_anomaly()
