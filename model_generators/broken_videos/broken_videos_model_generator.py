import numpy as np
import cv2
import os
import sys
from model_generators.model_generator import ModelGenerator
from model_generators.broken_videos.yandex_video_cutter import YandexVideoCutter


class BrokenVideosModelGenerator(ModelGenerator):
    def __init__(self, video_cutter):
        self.__video_cutter = video_cutter

    def _save_video_model(self, model):
        output_directory = os.path.join(os.path.join(os.path.dirname(__file__), "model_broken_videos"))
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        np.save(os.path.join(output_directory, "model_broken_videos.npy"), model)
        return os.path.abspath(output_directory)

    def generate(self, paths2data, extensions):
        video_frames = []
        for path2data in paths2data:
            for ext in extensions:
                video_frames.extend(self.__video_cutter.cut(path2data, ext))
        num = 0
        hist_gen = np.zeros((26, 1), dtype=np.float32)
        for frame in video_frames:
            frame = cv2.resize(frame, (159, 86))
            hist = cv2.calcHist([frame], [0], None, [26], [0, 256])
            hist_gen += hist
            num += 1
        hist_gen /= num
        results_dir = self._save_video_model(hist_gen)
        print("Saved results to {}/ \nBye!".format(results_dir))


if __name__ == '__main__':
    video_cutter = YandexVideoCutter()
    model_generator = BrokenVideosModelGenerator(video_cutter)
    path2data = [os.path.join(os.path.dirname(__file__), "../..", "data") + "/broken_imgs/bad/"]
    extensions = [".png"]
    if len(sys.argv) > 2:
        path2data = [sys.argv[1]]
        extensions = [sys.argv[2]]

    model_generator.generate(path2data, extensions)
