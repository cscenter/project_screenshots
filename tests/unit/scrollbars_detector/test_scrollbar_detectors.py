import os
import unittest

import cv2

from screenqual.core.screenshot import Screenshot
from screenqual.filter.scrollbars_detector import ScrollBarAnalyser


class TestScrollBarAnalyser(unittest.TestCase):
    def test_does_not_fire_on_good_pages(self):
        self.assert_no_scrollbars('imgs/without_scrollbars/1.png')

    def test_fires_on_screenshots_with_vertical_linux_scrollbars(self):
        self.assert_with_scrollbars('imgs/with_scrollbars/2.png')
        self.assert_with_scrollbars('imgs/with_scrollbars/3.png')

    def test_fires_on_screenshots_with_vertical_and_horizontal_windows_scrollbars(self):
        self.assert_with_scrollbars('imgs/with_scrollbars/4.png')

    def test_should_work_if_none_lines_returned_from_hough_lines_method(self):
        self.assert_no_scrollbars('imgs/without_scrollbars/none_lines.png')

    def assert_with_scrollbars(self, relarive_path):
        self.assertTrue(self._analyze(relarive_path))

    def assert_no_scrollbars(self, relarive_path):
        self.assertFalse(self._analyze(relarive_path))

    def _analyze(self, relative_path):
        base_path = os.path.join(os.path.dirname(__file__))
        img = cv2.imread(base_path + "/" + relative_path)
        return ScrollBarAnalyser().execute(Screenshot(img))
