from screenqual.filter.yandex_sans_detector.yandex_sans_detector import YandexSansDetector
from tests.regression.regression_test import TestRegression


class TestRegressionScrollbarDetector(TestRegression):
    def test_fscore_on_scrollbar_detector(self):
        self.fscore(["/ys/arial/"], ["/ys/ys/"],
                    YandexSansDetector(), .85, "yandex detector")
