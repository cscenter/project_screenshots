import unittest
from glob import glob
import cv2
from screenshots.screenshot_filters.text_near_edge_detector import TextNearEdgeDetector
from screenshots.core.screenshot import Screenshot
import os


class TestTextNearEdgeDetector(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.join(os.path.dirname(__file__))

    def test_does_not_fire_on_good_text_document_screenshots(self):
        dtor = TextNearEdgeDetector()
        path = self.base_path + "/ok.png"
        print(path)
        img = cv2.imread(path)
        screenshot = Screenshot(img, None, None, None)
        self.assertFalse(dtor.execute(screenshot))

    def test_fires_on_bad_text_document_screenshots(self):
        dtor = TextNearEdgeDetector()
        path = self.base_path + "/text_on_edge.png"
        img = cv2.imread(path)
        screenshot = Screenshot(img, None, None, None)
        self.assertTrue(dtor.execute(screenshot), "Failed at {0}".format(path))
