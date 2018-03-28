import unittest
import cv2
from screenqual.filter.scrollbars_detector import ScrollBarAnalyser
from screenqual.core.screenshot import Screenshot
import os


class TestScrollBarAnalyser(unittest.TestCase):
    def setUp(self):
        self.base_path = os.path.join(os.path.dirname(__file__))

    def test_does_not_fire_on_good_pages(self):
        scrdet = ScrollBarAnalyser()

        img1 = cv2.imread(self.base_path + "/imgs/without_scrollbars/1.png")
        screenshot1 = Screenshot(img1, None, None, [])
        self.assertFalse(scrdet.execute(screenshot1))

    def test_fires_on_screenshots_with_vertical_linux_scrollbars(self):
        scrdet = ScrollBarAnalyser()

        img2 = cv2.imread(self.base_path + "/imgs/with_scrollbars/2.png")
        screenshot2 = Screenshot(img2, None, None, [])
        self.assertTrue(scrdet.execute(screenshot2))

        img3 = cv2.imread(self.base_path + "/imgs/with_scrollbars/3.png")
        screenshot3 = Screenshot(img3, None, None, [])
        self.assertTrue(scrdet.execute(screenshot3))

    def test_fires_on_screenshots_with_vertical_and_horizontal_windows_scrollbars(self):
        scrdet = ScrollBarAnalyser()

        img4 = cv2.imread(self.base_path + "/imgs/with_scrollbars/4.png")
        screenshot4 = Screenshot(img4, None, None, [])
        self.assertTrue(scrdet.execute(screenshot4))