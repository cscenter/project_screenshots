from model_generators.broken_videos.video_cutter import VideoCutter
from screenqual.filter.broken_areas.broken_areas_analyser import BrokenAreasAnalyser
from glob import glob
import cv2


class YandexVideoCutter(BrokenAreasAnalyser):
    def __init__(self):
        BrokenAreasAnalyser.__init__(self)

    def cut(self, paths2data, extensions):
        filenames = glob(paths2data + "*" + extensions)
        video_frames = []
        for filename in filenames:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.INTERSECT_FULL)
            w, h = img.shape[:2]
            min_area = self._get_min_area(w, h)
            max_area = self._get_max_area(w, h)
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                if self._is_cnt_rect(approx):
                    area = cv2.contourArea(approx)
                    if min_area <= area <= max_area:
                        # Finds a play icon inside  video in order to separate them from broken images
                        _, thresh_ins = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
                        bounding_rect = self._get_rect_from_cnt(approx)
                        roi = self._cut_rectangle_from_img(thresh_ins, bounding_rect)
                        _, contours_ins, _ = cv2.findContours(roi, cv2.RETR_LIST, cv2.INTERSECT_FULL)
                        for cnt_ins in contours_ins:
                            approx_ins = cv2.approxPolyDP(cnt_ins, 0.01 * cv2.arcLength(cnt, True), True)
                            if len(approx_ins) == 3:
                                roi_gray = self._cut_rectangle_from_img(gray, bounding_rect)
                                video_frames.append(roi_gray)
        return video_frames
