import numpy as np
import cv2
from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.core.analyser_result import AnalyserResult
from screenqual.util.rectangle import Rectangle


class WhiteAreasAnalyser(ScreenshotAnalyser):

    def __init__(self, max_white_area=0.5):
        self.__max_white_area = max_white_area

    def execute(self, screenshot):
        img = screenshot.image
        kRescaleFactor = 0.5
        h, w = img.shape[:2]
        w = int(float(w) * kRescaleFactor)
        h = int(float(h) * kRescaleFactor)
        img = cv2.resize(img, (w, h))
        # Image pre-processing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        # Getting not white area to be filled with black
        kernel = np.ones((20, 20), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.dilate(thresh, kernel)
        h, w = img.shape[:2]
        dp = np.zeros((h, w, 2), dtype=np.int32)
        no_white_rect = -1
        # Filing the initial states for dp
        if thresh[0][0] != 0:
            dp[0][0][0] = no_white_rect
            dp[0][0][1] = no_white_rect

        for i in range(1, w):
            if thresh[0][i] == 0:
                if dp[0][i - 1][0] != no_white_rect:
                    dp[0][i][0] = dp[0][i - 1][0] + 1
                else:
                    dp[0][i][0] = 0
                    dp[0][i][1] = 0
            else:
                dp[0][i][0] = no_white_rect
                dp[0][i][1] = no_white_rect
        for i in range(1, h):
            if thresh[i][0] == 0:
                if dp[i][0][1] != no_white_rect:
                    dp[i][0][1] = dp[i - 1][0][1] + 1
                else:
                    dp[i][0][0] = 0
                    dp[i][0][1] = 0
            else:
                dp[i][0][0] = no_white_rect
                dp[i][0][1] = no_white_rect

        max_sq = 0
        # Dynamic for every pixel store the largest rectangle finishing in it
        for i in range(h):
            for j in range(w):
                if thresh[i][j] == 0:
                    if dp[i - 1][j][1] != no_white_rect and dp[i][j - 1][0] != no_white_rect:
                        dp[i][j][0] = min(dp[i][j - 1][0] + 1, dp[i - 1][j - 1][0] + 1)
                        dp[i][j][1] = min(dp[i - 1][j][1] + 1, dp[i - 1][j - 1][1] + 1)

                        cur_sq = dp[i][j][0] * dp[i][j][1]
                        if cur_sq > max_sq:
                            max_sq = cur_sq
                    else:
                        dp[i][j][0] = 0
                        dp[i][j][1] = 0
                else:
                    dp[i][j][0] = no_white_rect
                    dp[i][j][1] = no_white_rect
        all_white = (thresh == 0).sum()
        white_area = float(max_sq) / all_white
        if white_area > self.__max_white_area:
            return AnalyserResult.with_anomaly()
        return AnalyserResult.without_anomaly()
