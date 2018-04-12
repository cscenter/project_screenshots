from screenqual.filter.banner_detector import BannerAnalyser
from tests.regression.regression_test import TestRegression


class TestRegressionBanner(TestRegression):
    def test_fscore_banner_images(self):
        self.fscore(["/banner/with_banner/"], ["/banner/without_banner/"],
                    BannerAnalyser(), .8, "banner detector", extension="jpg")
