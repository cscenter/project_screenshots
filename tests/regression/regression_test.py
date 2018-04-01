from glob import glob
import cv2
from screenqual.core.screenshot import Screenshot
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator
from tests import DATA_ROOT


class TestRegression:
    def process_path(self, path, is_positive, detector, pr_calculator):
        filenames = glob(path + "*.png")
        for filename in filenames:
            img = cv2.imread(filename)
            screenshot = Screenshot(img, None, None, [])
            pr_calculator.expected(is_positive).found(detector.execute(screenshot))


    def test_fscore(self, paths_with_anomaly, paths_without_anomaly, filter):
        paths_with_anomaly = [DATA_ROOT + el for el in paths_with_anomaly]
        paths_without_anomaly = [DATA_ROOT + el for el in paths_without_anomaly]
        pr_calculator = PrecisionRecallCalculator()
        for path in paths_with_anomaly:
            self.process_path(path, True, filter, pr_calculator)
        for path in paths_without_anomaly:
            self.process_path(path, False, filter, pr_calculator)
        print(pr_calculator)
