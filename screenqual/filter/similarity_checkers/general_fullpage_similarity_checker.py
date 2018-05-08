from screenqual.filter.similarity_checkers.similarity_checker import SimilarityChecker
import numpy as np
import os


class GeneralFullpageSimilarityChecker(SimilarityChecker):
    def __init__(self, threshold=1200):
        base_path = os.path.join(os.path.dirname(__file__))
        self.__avg_spectre = np.load(os.path.join(base_path, "models", "yandex_fullpage_w_and_wo_header_avg_spectrum.npy"))
        self.__spectre_indicies = np.load(os.path.join(base_path, "models", "yandex_fullpage_w_and_wo_header_spectrum_indices.npy"))
        self.__threshold = threshold

    def _avg_spectrum(self):
        return self.__avg_spectre

    def _spectrum_indices(self):
        return self.__spectre_indicies

    def _threshold(self):
        return self.__threshold