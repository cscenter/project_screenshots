from screenqual.filter.banner_detector import BannerAnalyser
from tests.unit.unit_test import UnitTest


class TestBannerDetector(UnitTest):
    def setUp(self):
        self.analyser = BannerAnalyser()

    # def test_img_without_banner(self):
    #     self.assert_no_anomaly('banner_detector/img/without_banner/1.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/2.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/3.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/4.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/5.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/6.jpg')
    #     self.assert_no_anomaly('banner_detector/img/without_banner/7.jpg')

    def test_img_with_banner(self):
        self.assert_has_anomaly('banner_detector/img/with_banner/1.jpg')
        self.assert_has_anomaly('banner_detector/img/with_banner/2.jpg')
        self.assert_has_anomaly('banner_detector/img/with_banner/3.jpg')
        self.assert_has_anomaly('banner_detector/img/with_banner/4.jpg')
        self.assert_has_anomaly('banner_detector/img/with_banner/5.jpg')
        self.assert_has_anomaly('banner_detector/img/with_banner/6.jpg')
