# -*- coding: utf-8 -*-
'''
Данный скрипт вычисляет модель для сравнения скриншотов с коллекцией.

Запуск: python similarity_checker_model_generator.py absolute_path_to_collection file_extension_preceeded_with_dot

Результат: файлы со средним спектром коллеции и с индексами, необходимыми для сравнения, предлагаемое значение порога.

Известные проблемы:
1. предлагаемое значение порога может быть завышенным, что приведёт к увеличению количества FN.
Предлагается провести эксперименты на большой коллекции для точного определения порога,
2. относительно высокая требовательность к ресурсам.

'''



from model_generator import ModelGenerator
import cv2
import numpy as np
from glob import glob
import os
import sys
from random import shuffle


def _generate_spectrum(img_bgr, shape_cols_first):
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, shape_cols_first)
    spectrum = np.fft.fft2(img)
    fshift = np.fft.fftshift(spectrum)
    magnitude_spectrum = np.log(1 + np.abs(fshift))
    return magnitude_spectrum


def _save_spectrum(avg_spectrum, spectrum_indices):
    output_directory = os.path.join(os.path.join(os.path.dirname(__file__), "similarity_checker_model"))
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    np.save(os.path.join(output_directory, "avg_spectrum.npy"), avg_spectrum)
    np.save(os.path.join(output_directory, "spectrum_indices.npy"), spectrum_indices)
    return os.path.abspath(output_directory)


def _estimate_threshold(spectra, avg_spectrum, spectrum_indices):
    spdiff = np.abs(spectra - np.tile(avg_spectrum[:, :, np.newaxis], (1, 1, spectra.shape[2])))
    spdiff[spectrum_indices == 0, :] = 0
    sum_diff = spdiff.sum(axis=0).sum(axis=1)
    return np.percentile(sum_diff, 97) * 1.1


class SimilarityCheckerModelGenerator(ModelGenerator):
    '''
    spectrum_shape -- целевой размер для даунскейла. Чем он больше, тем дольше всё будет считать, но, вероятно, точнее.
    Разумно выбирать его пропорциональным размеру скриншота. Сначала указана ширина, затем высота.
    use_percentile -- какой процент значений спектра с минимальной вариацией использовать. Чем он меньше, тем больше оверфиттимся на
    конкретную коллекцию. Оптимальные значения находятся в интервале 0.1 ... 15 в зависимости от потребностей.
    train_split -- какую часть использовать для вычисления среднего спектра. Остальное идёт на вычисление порога.
    '''
    def __init__(self, spectrum_shape=(300, 600), use_percentile=0.3, train_split=0.7):
        self.__spectrum_shape = spectrum_shape
        self.__use_percentile = use_percentile
        self.__train_split = train_split

    def generate(self, paths2data, extensions):
        filenames = []
        for path2data in paths2data:
            for ext in extensions:
                for name in glob(os.path.join(path2data, "*" + ext)):
                    filenames.append(name)
        shuffle(filenames)
        print("Processing", os.path.join("|".join(paths2data), "*" + "|".join(extensions)))
        print("Got", len(filenames), "files")
        spectra = []
        for i, filename in enumerate(filenames):
            if i % 20 == 0:
                print("Processed {} files out of {}...".format(i, len(filenames)))
            img_bgr = cv2.imread(filename, cv2.IMREAD_COLOR)
            spectra.append(_generate_spectrum(img_bgr, self.__spectrum_shape))
        spectra = np.dstack(spectra)
        print("Aggregating results...")
        split = int(spectra.shape[-1] * self.__train_split)
        test = spectra[:, :, split:]
        spectra = spectra[:, :, :split]
        avg_spectrum = np.median(spectra, axis=2)
        spectra_sd = np.std(spectra - np.tile(avg_spectrum[:, :, np.newaxis], (1, 1, spectra.shape[2])), axis=2)
        spectra_sd[spectra_sd > np.percentile(spectra_sd, self.__use_percentile)] = 0
        spectra_sd[spectra_sd > 0] = 1
        spectra_sd = spectra_sd.astype(np.uint8)
        print("Estimating threshold...")
        est_threshold = _estimate_threshold(test, avg_spectrum, spectra_sd)
        print("Recommended threshold is {}".format(est_threshold))
        print("Done!")
        results_dir = _save_spectrum(avg_spectrum, spectra_sd)
        print("Saved results to {}/ \nBye!".format(results_dir))

if __name__ == "__main__":
    model_generator = SimilarityCheckerModelGenerator()
    path2data = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/fullpage_train/"))]
    extensions = [".png"]
    if len(sys.argv) > 2:
        path2data = [sys.argv[1]]
        extension = [sys.argv[2]]

    model_generator.generate(path2data, extensions)
