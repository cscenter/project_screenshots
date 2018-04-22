# -*- coding: utf-8 -*-
from glob import glob
import os
import cv2
import codecs
import numpy as np

from model_generators.model_generator import ModelGenerator
from screenqual.filter.yandex_sans_detector.util.features_extraction import extract_letters
from screenqual.filter.yandex_sans_detector.util.features_extraction import extract_patches


def _collect_letters(glob_mask):
    all_patches = []
    for filename in glob(glob_mask)[:1]:
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        patches = extract_patches(img)[:1]
        all_patches += patches
    letters = extract_letters(all_patches, 28)
    return letters


def _collect_ys_letters():
    DATA_ROOT = os.path.join(os.path.dirname(__file__), "../..", "data")
    mask = os.path.join(DATA_ROOT, "ys", "*_ys_.png")
    return _collect_letters(mask)

def _collect_not_ys_letters():
    DATA_ROOT = os.path.join(os.path.dirname(__file__), "../..", "data")
    mask = os.path.join(DATA_ROOT, "ys", "*_arial_.png")
    return _collect_letters(mask)

def _calculate_distances(letters_a, letters_b):
    common_keys = list(set(letters_a).intersection(letters_b))
    distances = np.array([cv2.absdiff(letters_a[k], letters_b[k]).sum() for k in common_keys])
    return common_keys, distances

class YandexSansModelGenerator(ModelGenerator):
    def generate(self):
        ys = _collect_ys_letters()
        # notys = _collect_not_ys_letters()
        keys = [u'а', u'с']
        letters = np.dstack([ys[k] for k in keys])
        np.save("letters.npy", letters)
        with codecs.open("labels.txt", encoding='utf-8', mode="w") as lab_file:
            lab_file.writelines(u"\n".join(keys))


if __name__ == "__main__":
    YandexSansModelGenerator().generate()