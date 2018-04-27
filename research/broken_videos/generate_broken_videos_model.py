import numpy as np
import cv2
import os
from glob import glob
from screenqual.util.rectangle import Rectangle
import math


def cut_videos(input_path, output_path):
    filenames = glob(input_path + "*.png")
    num = 0
    for filename in filenames:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        # Cut out edges not to consider them
        _, contours, _ = cv2.findContours(thresh, 1, 2)
        w, h = img.shape[:2]
        min_area = w * h * 0.002
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            # A rectangular case
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if area >= min_area:
                    _, thresh_ins = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
                    x_vals = approx[:, 0, 0]
                    y_vals = approx[:, 0, 1]
                    bounding_rect = Rectangle(x=x_vals.min() + 5, y=y_vals.min() + 5,
                                              w=x_vals.max() - x_vals.min() - 10,
                                              h=y_vals.max() - y_vals.min() - 10)
                    roi = thresh_ins[bounding_rect.y_upper_left:bounding_rect.y_bottom_right,
                          bounding_rect.x_upper_left:bounding_rect.x_bottom_right]
                    _, contours_ins, _ = cv2.findContours(roi, 1, 2)
                    for cnt_ins in contours_ins:
                        approx_ins = cv2.approxPolyDP(cnt_ins, 0.01 * cv2.arcLength(cnt, True), True)
                        if len(approx_ins) == 3:
                            roi_gray = gray[bounding_rect.y_upper_left:bounding_rect.y_bottom_right,
                                       bounding_rect.x_upper_left:bounding_rect.x_bottom_right]
                            cv2.imwrite(output_path + str(num) + ".png", roi_gray)
                            num += 1


def generate_model(input_path, output_file):
    filenames = glob(input_path + "*.png")
    num = 0
    hist_gen = np.zeros((26, 1), dtype=np.float32)
    for filename in filenames:
        img = cv2.imread(filename, 0)
        img = cv2.resize(img, (159, 86))
        hist = cv2.calcHist([img], [0], None, [26], [0, 256])
        hist_gen += hist
        num += 1
    hist_gen /= num
    np.save(output_file, hist_gen)


if __name__ == '__main__':
    # cut_videos(os.path.join(os.path.dirname(__file__), "../..", "data") + "/broken_imgs/bad/",
    #            os.path.join(os.path.dirname(__file__), "../..", "research") + "/broken_videos/bad_cropped/")

    generate_model(os.path.join(os.path.dirname(__file__), "../..", "research") + "/broken_videos/bad_cropped/",
                   os.path.join(os.path.dirname(__file__), "../..", "research") + "/broken_videos/model")
