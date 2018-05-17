from abc import ABCMeta, abstractmethod


class VideoCutter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def cut(self, paths2data, extensions):
        pass
