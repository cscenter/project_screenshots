# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


def _normalize(img):
    return img.astype(float) / 255.


def _pad(img, target_shape):
    target_image = img
    if img.shape[0] < target_shape[0]:
        pad_width = target_shape[0] - img.shape[0]
        target_image = cv2.copyMakeBorder(target_image, 0, pad_width, 0, 0, cv2.BORDER_REFLECT)
    if img.shape[1] < target_shape[1]:
        pad_width = target_shape[1] - img.shape[1]
        target_image = cv2.copyMakeBorder(img, 0, 0, 0, pad_width, cv2.BORDER_REFLECT)
    return target_image


def _area_may_contain_text(img):
    white_number = (np.sum(img, axis=2) > 600).sum()
    return white_number <= .95 * img.shape[0] * img.shape[1]


class YandexSansVsArialDetector(ScreenshotAnalyser):
    def __init__(self, overlap=0.2, lower_det_thresh=0.3, upper_det_thresh=0.7):
        path2model = os.path.join(os.path.dirname(__file__), "ys_nn_model.hdf5")
        self.__model = load_model(path2model)
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
                    imgs.append(_normalize(img_cut))


        X = np.stack(imgs, axis=3)
        X = np.rollaxis(X, 3, 0)
        preds = self.__model.predict(X)
        notys = np.sum(preds[:, 0] <= self.__lower_det_thresh)
        undecided = np.sum(np.logical_and(preds[:, 0] > self.__lower_det_thresh, preds[:, 0] <= self.__upper_det_thresh))
        ys = np.sum(preds[:, 0] > self.__upper_det_thresh)

        info = {"ys": int(ys), "notys": int(notys), "undecided": int(undecided)}
        print(info)
        # print(np.median(preds, axis=0))
        if max(ys, notys) > undecided:
            if ys > notys:
                return AnalyserResult.without_anomaly(info)
            else:
                return AnalyserResult.with_anomaly(info)
        else:
            return AnalyserResult.without_anomaly(info)
