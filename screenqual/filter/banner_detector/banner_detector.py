import os
import cv2

from screenqual.filter.banner_detector.model.neural_network import model_classify
from screenqual.core.analyser_result import AnalyserResult
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser


class BannerDetector(ScreenshotAnalyser):
    def __init__(self):
        super(ScreenshotAnalyser, self).__init__()
        path_to_weights = os.path.join(os.path.dirname(__file__), "model/weights_sign1.hdf5")
        self.__model = model_classify()
        self.__model.load_weights(path_to_weights)

    def execute(self, screenshot):
        h, w, _ = screenshot.image.shape
        model_input_shape = tuple([1, *self.__model.layers[0].input_shape[1:]])
        img = screenshot.image
        if w > h:
            w //= 3
        else:
            h = w // 3

        img = cv2.resize(img[:h, -w:], (100, 100)).reshape(model_input_shape) / 255.
        banner_probability = self.__model.predict(img)[0]
        is_banner = banner_probability.argmax(axis=0)
        if is_banner:
            return AnalyserResult.with_anomaly()#{"probability": banner_probability[1]})
        return AnalyserResult.without_anomaly()#{"probability": banner_probability[0]})