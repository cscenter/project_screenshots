from abc import ABCMeta, abstractmethod
import os
import screenqual


class ScreenshotAnalyser:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.path2models = os.path.join(os.path.dirname(screenqual.__file__), "models")

    @abstractmethod
    def execute(self, screenshot):
        pass
