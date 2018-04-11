from screenqual.filter.general_detector import GeneralDetector
from tests.unit.unit_test import UnitTest


class TestGeneralDetector(UnitTest):
    def setUp(self):
        self.analyser = GeneralDetector()

    def test_does_not_fire_on_good_screenshot1(self):
        self.assert_no_anomaly("general_detector/good1.png")

    def test_does_not_fire_on_good_screenshot2(self):
        self.assert_no_anomaly("general_detector/good2.png")

    def test_does_not_fire_on_white_areas(self):
        self.assert_no_anomaly("general_detector/lotofwhite.png")

    def test_does_not_fire_on_yandex_main_screenshot(self):
        self.assert_no_anomaly("general_detector/yndx_main.png")

    def test_fires_on_mostly_white_screenshot(self):
        self.assert_has_anomaly("general_detector/mostly_white.png")

    def test_fires_on_white_screenshot(self):
        self.assert_has_anomaly("general_detector/white.png")

