import os
import unittest

import cv2

from screenqual.core.screenshot import Screenshot

# Base class for all unit tests run on different filters
class UnitTest(unittest.TestCase):
    def assert_has_anomaly(self, analyser, relative_path):
        self.assertTrue(self._analyze(analyser, relative_path))

    def assert_no_anomaly(self, analyser, relative_path):
        self.assertFalse(self._analyze(analyser, relative_path))

    def _analyze(self, analyser, relative_path):
        base_path = os.path.join(os.path.dirname(__file__))
        img = cv2.imread(base_path + "/" + relative_path)
        return analyser.execute(Screenshot(img, None, None, []))
