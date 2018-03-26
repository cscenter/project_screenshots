import unittest
from glob import glob
import cv2
from screenshots.screenshot_filters.text_near_edge_detector import TextNearEdgeDetector
from screenshots.utils.screenshot import Screenshot


class TestTextNearEdgeDetector(unittest.TestCase):
    def test_does_not_fire_on_good_text_document_screenshots(self):
        filenames = glob("imgs/ok/text/*.png")
        dtor = TextNearEdgeDetector()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, None)
            self.assertFalse(dtor.execute(screenshot))

    def test_fires_on_bad_text_document_screenshots(self):
        filenames = glob("imgs/notok/text/text_on_edge/*.png")
        dtor = TextNearEdgeDetector()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, None)
            self.assertTrue(dtor.execute(screenshot), "Failed at {0}".format(path))
