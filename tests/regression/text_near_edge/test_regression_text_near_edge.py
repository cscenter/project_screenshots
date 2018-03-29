import unittest
from glob import glob
import cv2
from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
from tests import DATA_ROOT


class TestRegressionTextNearEdgeDetector(unittest.TestCase):
    def process_path(self, path, is_positive, detector, pr_calculator):
        filenames = glob(path + "*.png")

        for filename in filenames:
            img = cv2.imread(filename)
            screenshot = Screenshot(img, None, None, None)
            pr_calculator.expected(is_positive).found(detector.execute(screenshot))

    def process_paths(self, positive_paths, negative_paths, detector, pr_calculator):
        for path in positive_paths:
            self.process_path(path, True, detector, pr_calculator)

        for path in negative_paths:
            self.process_path(path, False, detector, pr_calculator)

    def test_fscore_on_desktop_text_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/desktop/text/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/desktop/text/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: desktop, text")
        dtor = TextNearEdgeDetector()
        self.process_paths(positive_paths, negative_paths, dtor, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .9)

    def test_fscore_on_mobile_text_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/mobile/text/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/mobile/text/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: mobile, text")
        dtor = TextNearEdgeDetector()
        self.process_paths(positive_paths, negative_paths, dtor, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .9)

    def test_fscore_on_desktop_verticals_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/desktop/verticals/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/desktop/verticals/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: desktop, verticals")
        dtor = TextNearEdgeDetector()
        self.process_paths(positive_paths, negative_paths, dtor, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .9)

    def test_fscore_on_mobile_verticals_documents(self):
        positive_paths = [
            DATA_ROOT + "/document_screenshots_cut/mobile/verticals/"
        ]

        negative_paths = [
            DATA_ROOT + "/document_screenshots/mobile/verticals/"
        ]

        pr_calculator = PrecisionRecallCalculator("text near edge: mobile, verticals")
        dtor = TextNearEdgeDetector()
        self.process_paths(positive_paths, negative_paths, dtor, pr_calculator)

        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > .9)