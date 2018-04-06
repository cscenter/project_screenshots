import os
import unittest

import cv2

from screenqual.core.screenshot import Screenshot


# Base class for all unit tests run on different filters

class UnitTest(unittest.TestCase):
    def set_analyser(self, analyser):
        self.analyser = analyser

    def assert_has_anomaly(self, relative_path):
        self.assertTrue(self._analyze(self.analyser, relative_path).has_anomaly)

    def assert_no_anomaly(self, relative_path):
        self.assertFalse(self._analyze(self.analyser, relative_path).has_anomaly)

    def _analyze(self, analyser, relative_path):
        base_path = os.path.join(os.path.dirname(__file__))
        img = cv2.imread(base_path + "/" + relative_path)
        return analyser.execute(Screenshot(img))
