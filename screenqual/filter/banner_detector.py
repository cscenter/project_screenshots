from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
from util.neural_network import model_classify
import cv2
import os


class BannerAnalyser(ScreenshotAnalyser):
    def __init__(self):
        super(ScreenshotAnalyser, self).__init__()
        path_to_model = os.path.join(os.path.dirname(__file__), "../../util/model/weights_sign.hdf5")
        self.model = model_classify()
        self.model.load_weights(path_to_model)

    def execute(self, screenshot):
        img_w = screenshot.image.shape[1]//3
        img = cv2.resize(screenshot.image[:img_w, :], (100, 100)).reshape((1, 100, 100, 3))/255
        banner_probability = self.model.predict(img)[0]
        is_banner = banner_probability.argmax(axis=0)
        print(banner_probability, is_banner)
        if is_banner:
            return AnalyserResult.with_anomaly({"probability": banner_probability[1]})
        return AnalyserResult.without_anomaly({"probability": banner_probability[0]})
