class Rectangle(object):

    def __init__(self, x, y, w, h):
        self.x_upper_left = x
        self.y_upper_left = y
        self.w = w
        self.h = h
        self.x_upper_right = x + w
        self.y_upper_right = y
        self.x_bottom_right = x + w
        self.y_bottom_right = y + h
        self.x_bottom_left = x
        self.y_bottom_left = y + h

    def get_area(self):
        return self.w * self.h
