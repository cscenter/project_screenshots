from glob import glob
import cv2
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
import os
import warnings

class TestRegression:

    def process_path(self, path, has_anomaly, detector, pr_calculator, extension):
        filenames = glob(path + "*." + extension)
        if len(filenames) == 0:
            warnings.warn("No files found at " + path, UserWarning)
        for filename in filenames:
            img = cv2.imread(filename)
            screenshot = Screenshot(img, None, None, [])
            pr_calculator.expected(has_anomaly).found(detector.execute(screenshot))


    def fscore(self, paths_with_anomaly, paths_without_anomaly,
               filter, f_score, pr_calculator_name,
               extension = "png"):
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
