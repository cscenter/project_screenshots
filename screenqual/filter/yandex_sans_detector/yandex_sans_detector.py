# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import codecs
from screenqual.filter.yandex_sans_detector.util.features_extraction import extract_letters, extract_patches
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class YandexSansDetector(ScreenshotAnalyser):
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "model")
        with codecs.open(os.path.join(model_path, "labels.txt"), encoding='utf-8') as labels_file:
            labels = [s.strip() for s in labels_file.readlines()]
        letters = np.load(os.path.join(model_path, "letters.npy"))
        self.__model = dict(zip(labels, np.rollaxis(letters, 2)))

    def execute(self, screenshot):
        img = cv2.cvtColor(screenshot.image, cv2.COLOR_BGR2GRAY)
        letters = extract_letters(extract_patches(img)[:3], 28)
        thresh = 640
        checked_at_least_one = False
        for k in self.__model:
            if k in letters:
                checked_at_least_one = True
                difference = (letters[k] == self.__model[k]).sum()
                if difference < thresh:
                     return AnalyserResult.with_anomaly("mismatch at letter {0} is {1}".format(k.encode("utf-8"), difference))
                else:
                    return AnalyserResult.without_anomaly()
        return AnalyserResult.without_anomaly({"warning": "Couldn't fine a letter to compare against"})


