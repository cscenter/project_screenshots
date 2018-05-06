from screenqual.filter.yandex_sans_vs_arial_detector.yandex_sans_vs_arial_detector import YandexSansVsArialDetector
from tests.regression.regression_test import TestRegression


class TestRegressionScrollbarDetector(TestRegression):
    def test_fscore_on_scrollbar_detector(self):
        self.fscore(["/ys/helvetica/"], ["/ys/ys/"],
                    YandexSansVsArialDetector(), .85, "yandex sans detector", "jpg")
