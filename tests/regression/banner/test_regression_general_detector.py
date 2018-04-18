from screenqual.filter.general_detector import GeneralDetector
from tests.regression.regression_test import TestRegression


class TestRegressionGeneralDetector(TestRegression):
    def test_fscore_on_desktop_screenshots(self):
        self.fscore(["/general_fullpage/desktop/bad/"],
                    ["/general_fullpage/desktop/good/"],
                    GeneralDetector(), .9, "general detector: desktop")

    def test_fscore_on_mobile_screenshots(self):
        self.fscore(["/general_fullpage/mobile/bad/"],
                    ["/general_fullpage/mobile/good/"],
                    GeneralDetector(), .9, "general detector: mobile", "jpg")