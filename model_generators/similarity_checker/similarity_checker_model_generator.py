from model_generator import ModelGenerator
from screenqual.filter.similarity_checkers.similarity_checker import generate_spectrum
import cv2
import numpy as np
from glob import glob
import os
import sys
from random import shuffle


def _save_spectrum(avg_spectrum, spectrum_indices):
    output_directory = os.path.join(os.path.join(os.path.dirname(__file__), "similarity_checker_model"))
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    np.save("avg_spectrum.npy", avg_spectrum)
    np.save("spectrum_indices.npy", spectrum_indices)
    return os.path.abspath(output_directory)


def _estimate_threshold(spectra, avg_spectrum, spectrum_indices):
    spdiff = np.abs(spectra - np.tile(avg_spectrum[:, :, np.newaxis], (1, 1, spectra.shape[2])))
    spdiff[spectrum_indices == 0, :] = 0
    sum_diff = spdiff.sum(axis=0).sum(axis=1)
    return np.percentile(sum_diff, 97) * 1.1


class SimilarityCheckerModelGenerator(ModelGenerator):
    def __init__(self, spectrum_shape=(300, 600), use_percentile=0.3, train_split=0.7):
        """
        spectrum_shape -- target downscale size. The greater this size, the more accurate comparisons you get,
            in expense of increased computational time.
            It would be wise to choose this size to be proportional to the size of the screenshot.
            The first value of a tuple is the width, and the second one is the height.
        use_percentile -- sets the percentile of spectrum values with minimal variation will be used in spectra comparisons.
            The lower the percentile, the greater is the overfitting on the training collection. Optimal values are in range 0.1 ... 15.
            Choose the appropriate value for your needs.
        train_split -- sets the percent of the data to be used for training. The other part is used for the threshold estimation.
        """
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
            spectra.append(generate_spectrum(img_bgr, self.__spectrum_shape))
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
    path2data = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/fullpage_train/"))]
    extensions = [".png"]
    if len(sys.argv) > 2:
        path2data = [sys.argv[1]]
        extension = [sys.argv[2]]

    model_generator.generate(path2data, extensions)
