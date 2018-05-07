import cv2
import numpy as np
import os
from keras.models import load_model
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


def _normalize(img, min_x, max_x):
    img = img.astype(float) - min_x
    img /= np.maximum(1, (max_x - min_x))
    return img


def _pad(img, target_shape):
    target_image = img
    if img.shape[0] < target_shape[0]:
        pad_width = target_shape[0] - img.shape[0]
        target_image = cv2.copyMakeBorder(target_image, 0, pad_width, 0, 0, cv2.BORDER_REFLECT)
    if img.shape[1] < target_shape[1]:
        pad_width = target_shape[1] - img.shape[1]
        target_image = cv2.copyMakeBorder(target_image, 0, 0, 0, pad_width, cv2.BORDER_REFLECT)
    return target_image


def _area_may_contain_text(img):
    white_number = (np.sum(img, axis=2) > 600).sum()
    return white_number <= .95 * img.shape[0] * img.shape[1]


class YandexSansVsArialDetector(ScreenshotAnalyser):
    def __init__(self, overlap=0.2, lower_det_thresh=0.1, upper_det_thresh=0.8):
        path2model = os.path.dirname(__file__)
        self.__model = load_model(os.path.join(path2model, "ys_nn_model.hdf5"))
        self.__preproc_min = np.load(os.path.join(path2model, "min_x.npy"))
        self.__preproc_max = np.load(os.path.join(path2model, "max_x.npy"))
        self.__model_input_shape = self.__model.layers[0].input_shape[1:3]
        self.__step = tuple(int((1 - overlap) * dim) for dim in self.__model_input_shape)
        self.__lower_det_thresh = lower_det_thresh
        self.__upper_det_thresh = upper_det_thresh

    def execute(self, screenshot):
        img = screenshot.image
        img = _pad(img, self.__model_input_shape)
        imgs = []

        for row in range(0, img.shape[0], self.__step[0]):
            for col in range(0, img.shape[1], self.__step[1]):
                h, w = self.__model_input_shape
                if row + h <= img.shape[0] and col + w <= img.shape[1]:
                    img_cut = img[row:row + h, col:col + w]
                    # if _area_may_contain_text(img_cut):
                    imgs.append(_normalize(img_cut, self.__preproc_min, self.__preproc_max))

        X = np.stack(imgs, axis=3)
        X = np.rollaxis(X, 3, 0)
        preds = self.__model.predict(X)
        notys = np.sum(preds[:, 0] <= self.__lower_det_thresh)
        undecided = np.sum(np.logical_and(preds[:, 0] > self.__lower_det_thresh, preds[:, 0] <= self.__upper_det_thresh))
        ys = np.sum(preds[:, 0] > self.__upper_det_thresh)

        info = {"ys": int(ys), "notys": int(notys), "undecided": int(undecided)}
        # print(info)
        # print(np.median(preds, axis=0))
        if ys >= notys:
            return AnalyserResult.without_anomaly(info)
        else:
            return AnalyserResult.with_anomaly(info)
