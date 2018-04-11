from screenqual.filter.broken_images_detector import BrokenImagesAnalyser
from tests.unit.unit_test import UnitTest


class TestBrokenImagesDetector(UnitTest):
    def setUp(self):
        self.analyser = BrokenImagesAnalyser()

    def test_does_not_fire_on_good_screenshots(self):
        self.assert_no_anomaly("broken_images/imgs/ok/1.png")

    def test_does_not_fire_on_good_screenshots_2(self):
        self.assert_no_anomaly("broken_images/imgs/ok/2.png")

    def test_does_not_fire_on_good_screenshots_with_3(self):
        self.assert_no_anomaly(
            "broken_images/imgs/ok/https___yandex.ru_search_?text=mylittleponny.png")

    def test_does_not_fire_on_good_screenshots_with_4(self):
        self.assert_no_anomaly(
            "broken_images/imgs/ok/https___yandex.ru_search_?text=бололайка.png")

    def test_does_not_fire_on_good_screenshots_5(self):
        self.assert_no_anomaly(
            "broken_images/imgs/ok/https___yandex.ru_search_?text=волк.png")

    def test_does_not_fire_on_good_screenshots_6(self):
        self.assert_no_anomaly(
            "broken_images/imgs/ok/https___yandex.ru_search_?text=911.png")

    def test_fires_on_screenshots_with_bad_yandex_images(self):
        self.assert_has_anomaly("broken_images/imgs/not_ok/1.png")

    def test_fires_on_screenshots_with_bad_google_images(self):
        self.assert_has_anomaly("broken_images/imgs/not_ok/google2.png")

    def test_fires_on_screenshots_with_round_corners_images(self):
        self.assert_has_anomaly("broken_images/imgs/not_ok/google1.png")
