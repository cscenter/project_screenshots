import unittest
from screenqual.filter.broken_images_detector import BrokenImagesAnalyser
from tests.regression.regression_test import TestRegression

class TestRegressionBrokenImages(unittest.TestCase, TestRegression):
    def test_fscore_on_broken_images(self):
        self.fscore(["/broken_imgs/bad/"], ["/broken_imgs/good/"],
                    BrokenImagesAnalyser(), .88, "broken images detector")
