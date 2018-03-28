import unittest
from glob import glob
import cv2
from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
from tests import DATA_ROOT


class TestRegressionTextNearEdgeDetector(unittest.TestCase):
    def test_fscore_on_desktop_text_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/desktop/text/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/desktop/text/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: desktop, text")
        dtor = TextNearEdgeDetector()
        for path in positive_paths:
            filenames = glob(path + "*.png")

            for filename in filenames:
                img = cv2.imread(filename)
                screenshot = Screenshot(img, None, None, None)
                pr_calculator.expected(True).found(dtor.execute(screenshot))

        for path in negative_paths:
            filenames = glob(path + "*.png")
            for filename in filenames:
                img = cv2.imread(filename)
                screenshot = Screenshot(img, None, None, None)
                pr_calculator.expected(False).found(dtor.execute(screenshot))

        print(pr_calculator)

    def test_fscore_on_mobile_text_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/mobile/text/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/mobile/text/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: mobile, text")
        dtor = TextNearEdgeDetector()
        for path in positive_paths:
            filenames = glob(path + "*.png")

            for filename in filenames:
                img = cv2.imread(filename)
                screenshot = Screenshot(img, None, None, None)
                pr_calculator.expected(True).found(dtor.execute(screenshot))

        for path in negative_paths:
            filenames = glob(path + "*.png")
            for filename in filenames:
                img = cv2.imread(filename)
                screenshot = Screenshot(img, None, None, None)
                pr_calculator.expected(False).found(dtor.execute(screenshot))

        print(pr_calculator)
