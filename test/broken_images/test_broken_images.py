import unittest
from glob import glob
import cv2
from screenshot_filters.broken_images_detector import BrokenImagesAnalyser
from utils.screenshot import Screenshot


class TestBrokenImagesDetector(unittest.TestCase):
    def test_does_not_fire_on_good_pages(self):
        filenames = glob("imgs/ok/*.png")
        bia = BrokenImagesAnalyser()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, None)
            self.assertFalse(bia.execute(screenshot))

    def test_fires_on_screenshots_with_bad_images(self):
        filenames = glob("imgs/notok/*.png")
        bia = BrokenImagesAnalyser()
        for path in filenames:
            img = cv2.imread(path)
            screenshot = Screenshot(img, None, None, [])
            self.assertTrue(bia.execute(screenshot))
