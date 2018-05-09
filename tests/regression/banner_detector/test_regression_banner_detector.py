from screenqual.filter.banner_detector.banner_detector import BannerAnalyser
from tests.regression.regression_test import TestRegression


class TestRegressionBanner(TestRegression):
    def test_fscore_banner_images(self):
        self.fscore(["/banner_detector/with_banner/"], ["/banner_detector/without_banner/"],
                    BannerAnalyser(), .0, "banner_detector detector", extensions=["jpg"])
