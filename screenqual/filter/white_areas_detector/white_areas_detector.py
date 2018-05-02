import numpy as np
import cv2
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult


class WhiteAreasAnalyser(ScreenshotAnalyser):

    def __init__(self, max_white_area=0.5):
        self.__max_white_area = max_white_area

    class DpElementInfo():
        def __init__(self):
            self.height = 0
            self.width = 0
            self.__no_white_rect = -1

        def assign_rect_start(self):
            self.height = 0
            self.width = 0

        def set_no_white_rect(self):
            self.height = self.__no_white_rect
            self.width = self.__no_white_rect

        def is_width_no_white(self):
            return self.width != self.__no_white_rect

        def is_height_no_white(self):
            return self.height != self.__no_white_rect

    def execute(self, screenshot):
        img = screenshot.image
        k_rescale_factor = 0.5
        h, w = img.shape[:2]
        w = int(w * k_rescale_factor)
        h = int(h * k_rescale_factor)
        img = cv2.resize(img, (w, h))
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        # Getting not white area to be filled with black
        kernel = np.ones((20, 20), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.dilate(thresh, kernel)
        dp = np.ones((h, w), dtype=self.DpElementInfo)
        for i in range(h):
            for j in range(w):
                dp[i, j] = self.DpElementInfo()
        no_white_rect = -1

        # Filing the initial states for dp
        if thresh[0, 0] != 0:
            dp[0, 0].set_no_white_rect()

        for i in range(1, w):
            if thresh[0, i] == 0:
                if dp[0, i - 1].is_width_no_white():
                    dp[0, i].width = (dp[0, i - 1].width + 1)
                else:
                    dp[0, i].assign_rect_start()
            else:
                dp[0, i].set_no_white_rect()

        for i in range(1, h):
            if thresh[i, 0] == 0:
                if dp[i, 0].is_height_no_white():
                    dp[i, 0].height = (dp[i - 1, 0].height + 1)
                else:
                    dp[i, 0].assign_rect_start()
            else:
                dp[i, 0].set_no_white_rect()

        max_sq = 0
        max_h = 0
        max_w = 0
        max_w_idx = 0
        max_h_idx = 0
        # Dynamic for every pixel store the largest rectangle finishing in it
        for i in range(1, h):
            for j in range(1, w):
                if thresh[i, j] == 0:
                    if dp[i - 1, j].is_height_no_white() and dp[i, j - 1].is_width_no_white():
                        dp[i, j].width = (min(dp[i, j - 1].width + 1,
                                               dp[i - 1, j - 1].width + 1))
                        dp[i, j].height = (min(dp[i - 1, j].height + 1,
                                                dp[i - 1, j - 1].height + 1))

                        cur_sq = dp[i, j].width * dp[i, j].height
                        if cur_sq > max_sq:
                            max_sq = cur_sq
                            max_h = dp[i, j].height
                            max_w = dp[i, j].width
                            max_w_idx = j
                            max_h_idx = i
                    else:
                        dp[i, j].assign_rect_start()
                else:
                    dp[i, j].set_no_white_rect()

        all_white = (thresh == 0).sum()
        white_area = float(max_sq) / all_white
        white_area_info = {
            "max_sq": int(max_sq),
            "max_h": int(max_h),
            "max_w": int(max_w),
            "max_w_idx": max_w_idx,
            "max_h_idx": max_h_idx,
            "white_area_ratio": white_area
        }
        if white_area > self.__max_white_area:
            return AnalyserResult.with_anomaly(white_area_info)
        return AnalyserResult.without_anomaly(white_area_info)
