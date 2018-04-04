from screenqual.filter.text_near_edge_detector import TextNearEdgeDetector
from tests.regression.regression_test import TestRegression

class TestRegressionTextNearEdgeDetector(TestRegression):

    def test_fscore_on_desktop_text_documents(self):
        self.fscore(["/document_screenshots_cut/desktop/text/"],
                    ["/document_screenshots/desktop/text/"],
                    TextNearEdgeDetector(), .9, "text near edge: desktop, text")

    def test_fscore_on_mobile_text_documents(self):
        self.fscore(["/document_screenshots_cut/mobile/text/"],
                    ["/document_screenshots/mobile/text/"],
                    TextNearEdgeDetector(), .9, "text near edge: mobile, text")

    def test_fscore_on_desktop_verticals_documents(self):
        self.fscore(["/document_screenshots_cut/desktop/verticals/"],
                    ["/document_screenshots/desktop/verticals/"],
                    TextNearEdgeDetector(), .9, "text near edge: desktop, verticals")

    def test_fscore_on_mobile_verticals_documents(self):
        self.fscore(["/document_screenshots_cut/mobile/verticals/"],
                    ["/document_screenshots/mobile/verticals/"],
                    TextNearEdgeDetector(), .9, "text near edge: mobile, verticals")
