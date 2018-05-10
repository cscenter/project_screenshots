from screenqual.filter.screenshot_analyser import ScreenshotAnalyser
from screenqual.util.rectangle import Rectangle

class BrokenAreasAnalyser(ScreenshotAnalyser):

    def __init__(self):
        self.__min_area_ratio = 0.001
        self.__max_area_ratio = 0.5

    def _get_min_area(self, w, h):
        return self.__min_area_ratio * w * h

    def _get_max_area(self, w, h):
        return self.__max_area_ratio * w * h

    def _cut_rectangle_from_img(self, img, rect):
        return img[rect.y_upper_left:rect.y_bottom_right,
                  rect.x_upper_left:rect.x_bottom_right]

    def _get_rect_from_cnt(self, cnt):
        x_vals = cnt[:, 0, 0]
        y_vals = cnt[:, 0, 1]
        return Rectangle(x=x_vals.min() + 5, y=y_vals.min() + 5,
                         w=x_vals.max() - x_vals.min() - 10,
                         h=y_vals.max() - y_vals.min() - 10)

    def _is_cnt_rect(self, cnt):
        return len(cnt) == 4
