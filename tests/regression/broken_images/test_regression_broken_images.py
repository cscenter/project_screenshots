import unittest
from glob import glob
import cv2
from screenqual.filter.broken_images_detector import BrokenImagesAnalyser
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
from tests import DATA_ROOT
import os
from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector

class TestRegressionBrokenImages(unittest.TestCase):
    def process_path(self, path, is_positive, detector, pr_calculator):
        filenames = glob(path + "*.png")
        for filename in filenames:
            img = cv2.imread(filename)
            screenshot = Screenshot(img, None, None, [])
            pr_calculator.expected(is_positive).found(detector.execute(screenshot))

    def process_paths(self, positive_paths, negative_paths, detector, pr_calculator):
        for path in positive_paths:
            self.process_path(path, True, detector, pr_calculator)

        for path in negative_paths:
            self.process_path(path, False, detector, pr_calculator)

    def test_fscore_on_desktop_text_documents(self):
        positive_paths = [
            DATA_ROOT + "/broken_imgs/bad/"
        ]

        negative_paths = [
            DATA_ROOT + "/broken_imgs/good/"
        ]

        pr_calculator = PrecisionRecallCalculator("broken images detector:")
        bia = BrokenImagesAnalyser()
        self.process_paths(positive_paths, negative_paths, bia, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .88)
