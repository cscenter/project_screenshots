from screenqual.filter.broken_images_detector import BrokenImagesAnalyser
from tests.unit.unit_test import UnitTest


class TestBrokenImagesDetector(UnitTest):
    def setUp(self):
        self.bia = BrokenImagesAnalyser()

    def test_does_not_fire_on_good_screenshots(self):
        self.assert_no_anomaly(self.bia,
                               "broken_images/imgs/ok/1.png")
        self.assert_no_anomaly(self.bia,
                               "broken_images/imgs/ok/2.png")

    def test_fires_on_screenshots_with_bad_images(self):
        self.assert_has_anomaly(self.bia,
                                "broken_images/imgs/not_ok/1.png")
        self.assert_has_anomaly(self.bia,
                                "broken_images/imgs/not_ok/google2.png")
