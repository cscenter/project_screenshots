import unittest
from glob import glob
import cv2
from screenshot_filters.broken_images_detector import BrokenImagesAnalyser
from utils.screenshot import Screenshot


class TestBrokenImagesDetector(unittest.TestCase):

    def test_does_not_fire_on_good_pages(self):
        bia = BrokenImagesAnalyser()

        img1 = cv2.imread("imgs/ok/1.png")
        screenshot1 = Screenshot(img1, None, None, None)
        self.assertFalse(bia.execute(screenshot1))

        img2 = cv2.imread("imgs/ok/2.png")
        screenshot2 = Screenshot(img2, None, None, None)
        self.assertFalse(bia.execute(screenshot2))

    def test_fires_on_screenshots_with_bad_images(self):
        bia = BrokenImagesAnalyser()
        img = cv2.imread("imgs/not_ok/1.png")
        screenshot = Screenshot(img, None, None, [])
        self.assertTrue(bia.execute(screenshot))
