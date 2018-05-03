from glob import glob
import cv2
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
import os
import warnings
import unittest
import inspect


def _append_result(results, expected, found, path):
    if expected and found:
        results.append("TP:: " + path)
    elif not expected and found:
        results.append("FP:: " + path)
    elif expected and not found:
        results.append("FN:: " + path)
    else:
        results.append("TN:: " + path)


class TestRegression(unittest.TestCase):
    def setUp(self):
        self.results = []

    def tearDown(self):
        log_filename = os.path.splitext(inspect.getfile(self.__class__))[0] + "_" + self._testMethodName + ".log"
        with open(log_filename, "w") as log_file:
            for result in sorted(self.results):
                log_file.write(result + os.linesep)

    def process_path(self, path, has_anomaly, detector, pr_calculator, extension):
        filenames = glob(path + "*." + extension)
        if len(filenames) == 0:
            warnings.warn("No files found at " + path, UserWarning)

        for filename in filenames:
            img = cv2.imread(filename)
            screenshot = Screenshot(img)
            got_value = detector.execute(screenshot)
            _append_result(self.results, has_anomaly, got_value, filename)
            pr_calculator.expected(has_anomaly).found(got_value)

    def fscore(self, paths_with_anomaly, paths_without_anomaly,
               filter, f_score, pr_calculator_name,
               extension="png"):
        DATA_ROOT = os.path.join(os.path.dirname(__file__), "../..", "data")
        paths_with_anomaly = [DATA_ROOT + el for el in paths_with_anomaly]
        paths_without_anomaly = [DATA_ROOT + el for el in paths_without_anomaly]
        pr_calculator = PrecisionRecallCalculator(pr_calculator_name)
        for path in paths_with_anomaly:
            self.process_path(path, True, filter, pr_calculator, extension)
        for path in paths_without_anomaly:
            self.process_path(path, False, filter, pr_calculator, extension)
        print(pr_calculator)
        self.assertTrue(pr_calculator.fscore() > f_score)
