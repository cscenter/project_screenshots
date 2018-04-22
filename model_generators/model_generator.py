from abc import ABCMeta, abstractmethod


class ModelGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self):
        pass
