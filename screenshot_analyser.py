from abc import ABCMeta, abstractmethod

class ScreenshotAnalyser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, screenshot):
        pass
