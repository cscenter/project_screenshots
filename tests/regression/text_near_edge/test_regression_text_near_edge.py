import unittest
from glob import glob
import cv2
from screenshots.screenshot_filters.text_near_edge_detector import TextNearEdgeDetector
from screenshots.core.screenshot import Screenshot
from regression.precision_recall_calculator import PrecisionRecallCalculator
import os


class TestRegressionTextNearEdgeDetector(unittest.TestCase):
    def test_fscore_is_over_random(self):
        base_path = os.path.join(os.path.dirname(__file__))
        pr_calculator = PrecisionRecallCalculator()
        # estimate on negative
        filenames = glob(base_path + "/imgs/ok/text/*.png")
        dtor = TextNearEdgeDetector()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, None)
            pr_calculator.expected(False).found(dtor.execute(screenshot))

        # estimate on positive
        filenames = glob(base_path + "/imgs/notok/text/text_on_edge/*.png")
        dtor = TextNearEdgeDetector()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, None)
            pr_calculator.expected(True).found(dtor.execute(screenshot))

        print("Statistics for {0}".format(self.__class__.__name__))
        print("-" * len("Statistics for {0}".format(self.__class__.__name__)))
        print("{0:20s}: {1:.5f}".format("Precision: ", pr_calculator.precision()))
        print("{0:20s}: {1:.5f}".format("Recall: ", pr_calculator.recall()))
        print("{0:20s}: {1:.5f}".format("FScore: ", pr_calculator.fscore()))
