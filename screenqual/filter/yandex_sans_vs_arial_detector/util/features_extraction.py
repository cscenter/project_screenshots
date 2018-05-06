from pytesseract import pytesseract as pt
from collections import defaultdict
import cv2
import numpy as np


def _generate_bounding_boxes(img):
    pt_result = pt.image_to_boxes(img, lang="rus").splitlines()
    boxes = [[int(x) for x in y.split()[1:-1]] for y in pt_result]
    labels = [y.split()[0] for y in pt_result]
    boxes = np.array(boxes)
    return boxes, labels


def _cut_letters(boxes, labels, img, window_size):
    h, w = img.shape
    letters = defaultdict(list)
    for bbox, label in zip(boxes, labels):
        letter_img = img[(h - bbox[3]):(h - bbox[1]), bbox[0]:bbox[2]]

        if letter_img.shape[0] > 0 and letter_img.shape[1] > 0:
            let = cv2.resize(letter_img, (window_size, window_size))
            letters[label].append(let)
    return letters


def _compress_letters(letters):
    for k in letters:
        let = np.median(np.dstack(letters[k]), axis=2).astype(np.uint8)
        res, let = cv2.threshold(let, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        letters[k] = let
    return letters


def extract_letters(imgs, window_size):
    all_letters = defaultdict(list)
    for img in imgs:
        assert len(img.shape) == 2
        boxes, labels = _generate_bounding_boxes(img)
        letters = _cut_letters(boxes, labels, img, window_size)
        for letter in letters:
            all_letters[letter] += letters[letter]
    letters = _compress_letters(all_letters)
    return letters


def extract_patches(img):
    if img.shape[0] > img.shape[1]:
        nrows = img.shape[0]
        img = img[int(nrows * 0.25) : int(nrows * 0.75), :]
    step = max(100, img.shape[0] // 10)
    patches = []
    for i in range(0, img.shape[0], step):
        patches.append(img[i : i + step, :])
    return patches
