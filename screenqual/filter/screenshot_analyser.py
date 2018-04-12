from abc import ABCMeta, abstractmethod
import os
import screenqual


class ScreenshotAnalyser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, screenshot):
        pass
