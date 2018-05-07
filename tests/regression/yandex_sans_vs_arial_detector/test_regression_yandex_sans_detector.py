from screenqual.filter.yandex_sans_vs_arial_detector.yandex_sans_vs_arial_detector import YandexSansVsArialDetector
from tests.regression.regression_test import TestRegression
import cv2
import random


def _resize(filename, img):
    fx = random.gauss(1.0, 0.3)
    fy = fx + random.gauss(0.0, 0.1)
    fx = min(max(0.5, fx), 2.0)
    fy = min(max(0.5, fy), 2.0)
    return cv2.resize(img, None, fx=fx, fy=fy)


class TestRegressionYandexSansVsArialDetector(TestRegression):
    def test_fscore_on_ys_vs_arial(self):
        self.fscore(["/ys/arial/"], ["/ys/ys/"],
                    YandexSansVsArialDetector(), .9, "yandex sans detector: vs arial", "jpg", _resize)

    def test_fscore_on_ys_vs_helvetica(self):
        self.fscore(["/ys/helvetica/"], ["/ys/ys/"],
                    YandexSansVsArialDetector(), .9, "yandex sans detector: vs helvetica", "jpg", _resize)
