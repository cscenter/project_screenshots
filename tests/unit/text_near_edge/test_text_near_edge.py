from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector
from tests.unit.unit_test import UnitTest


class TestTextNearEdgeDetector(UnitTest):
    def setUp(self):
        self.analyser = TextNearEdgeDetector()

    def test_does_not_fire_on_good_text_document_screenshots(self):
        self.assert_no_anomaly("text_near_edge/ok.png")

    def test_fires_on_bad_text_document_screenshots(self):
        self.assert_has_anomaly("text_near_edge/text_on_edge.png")
