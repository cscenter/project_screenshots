import unittest
from glob import glob
import cv2
from screenqual.filter.scrollbars_detector import ScrollBarAnalyser
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
from tests import DATA_ROOT

class TestRegressionScrollbarDetector(unittest.TestCase):
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
            DATA_ROOT + "/scrollbars/with_scrollbars/"
        ]

        negative_paths = [
            DATA_ROOT + "/scrollbars/without_scrollbars/"
        ]

        pr_calculator = PrecisionRecallCalculator("scrollbars detector:")
        scran = ScrollBarAnalyser()
        self.process_paths(positive_paths, negative_paths, scran, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .88)
