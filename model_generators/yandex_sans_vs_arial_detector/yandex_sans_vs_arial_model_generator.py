from model_generator import ModelGenerator
from keras.models import Sequential
from keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense
from keras.callbacks import ModelCheckpoint
from collections import defaultdict
from glob import glob
import os
import cv2
import numpy as np
import sys


def _get_model(input_shape):
    model = Sequential()
    model.add(Conv2D(8, (3, 3), activation='relu', input_shape=(*input_shape, 3)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Dropout(0.05))

    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Dropout(0.05))

    model.add(Flatten())
    model.add(Dense(300, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(2, activation='softmax'))
    return model


class YandexSansVsArialModelGenerator(ModelGenerator):
    def __init__(self, target_size=(300, 300), train_split=0.8, nepochs=70):
        self.__train_split = train_split
        self.__target_size = target_size
        self.__nepochs = nepochs
        self.__keys = ["ys", "not_ys"]

    def _fetch_images(self, paths2data, extensions):
        imgs = defaultdict(list)
        for path in paths2data:
            for ext in extensions:
                for k in self.__keys:
                    for filename in glob(os.path.join(path, k, "*" + ext)):
                        img = cv2.imread(filename, cv2.IMREAD_COLOR)
                        for r in range(10):
                            row = np.random.randint(250, img.shape[0] - img.shape[0] // 3)
                            col = np.random.randint(100, img.shape[1] - 600)
                            w = np.random.randint(200, 400)
                            h = np.random.randint(200, 400)
                            if row + h < img.shape[0] and col + w < img.shape[1]:
                                img_cut = img[row:row + h, col:col + w]
                                img_cut = cv2.resize(img_cut, self.__target_size)
                                white_number = (np.sum(img_cut, axis=2) > 600).sum()
                                if white_number > .95 * img_cut.shape[0] * img_cut.shape[1]:
                                    continue
                                imgs[k].append(img_cut)
        return imgs

    def _convert2numpy(self, imgs):
        X = []
        y_values = []
        num_classes = 2

        for i, k in enumerate(self.__keys):
            X += imgs[k]
            y_values += [i] * len(imgs[k])

        X = np.stack(X, axis=3)
        X = np.rollaxis(X, 3, 0)
        y = np.zeros((X.shape[0], num_classes), np.int32)
        y[np.arange(len(y_values)), y_values] = 1
        print("Data shape: ", X.shape, y.shape)
        return X, y

    def _shuffle_and_normalize(self, X, y):
        idx = np.random.permutation(len(y))
        X = X[idx].astype(float)
        y = y[idx].astype(float)
        min_X = np.min(X, axis=0)
        max_X = np.max(X, axis=0)
        np.save("min_x.npy", min_X)
        np.save("max_x.npy", max_X)
        X[:] -= min_X
        X[:] /= np.maximum(1, (max_X - min_X))
        print("Classes: ", y[:, 0].sum(), y[:, 1].sum())
        return X, y

    def _compile_model(self, model):
        model.compile(loss="categorical_crossentropy",
                      optimizer="adam",
                      metrics=['accuracy'])

    def _train_model(self, model, X, y):
        checkpointer = ModelCheckpoint(filepath="yandex_sans_model.hdf5", verbose=1,
                                       save_best_only=True, save_weights_only=False)

        history = model.fit(X, y,
                            epochs=self.__nepochs,
                            batch_size=10,
                            shuffle=True,
                            verbose=1,
                            validation_split=1 - self.__train_split,
                            callbacks=[checkpointer])

    def generate(self, paths2data, extensions):
        imgs = self._fetch_images(paths2data, extensions)
        X, y = self._convert2numpy(imgs)
        X, y = self._shuffle_and_normalize(X, y)
        model = _get_model(self.__target_size)
        self._compile_model(model)
        self._train_model(model, X, y)

if __name__ == "__main__":
    model_generator = YandexSansVsArialModelGenerator()
    path2data = None
    extensions = None
    if len(sys.argv) > 2:
        path2data = [sys.argv[1]]
        extensions = [sys.argv[2]]
    else:
        print("Path to data expected", file=sys.stderr)
        exit(1)
    model_generator.generate(path2data, extensions)
