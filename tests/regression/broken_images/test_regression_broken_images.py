import unittest
from screenqual.filter.broken_images_detector import BrokenImagesAnalyser
from tests.regression.regression_test import TestRegression

class TestRegressionBrokenImages(unittest.TestCase, TestRegression):

    def run(self):
        bia = BrokenImagesAnalyser()
        self.test_fscore(["/broken_imgs/bad/"], ["/broken_imgs/good/"], bia, 0.88)

