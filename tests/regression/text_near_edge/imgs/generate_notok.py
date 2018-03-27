import cv2
import numpy as np
from glob import glob
import random

for fullimg_path in glob("fullpage/*.png"):
    filename = fullimg_path.strip(".png").strip("fullpage/")
    img = cv2.imread(fullimg_path)
    yoffset = 100
    cnt = 0
    while yoffset < 1500:
        height = random.randint(50, 150)
        loc_img = img[yoffset:(yoffset + height), 100:700]
        cv2.imshow("img", loc_img)
        cv2.imwrite("notok/{0}_{1}.png".format(filename, cnt), loc_img)
        cnt += 1
        yoffset += random.randint(50, 150)
