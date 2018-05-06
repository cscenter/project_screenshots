from keras.models import Sequential
from keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Dropout, Flatten, Dense

def __get_model(input_shape):
    model = Sequential()
    model.add(Conv2D(8, (3, 3), activation='relu', input_shape=self.__input_shape))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Conv2D(8, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Dropout(0.05))

    model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(BatchNormalization())
    # model.add(Conv2D(16, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(5, 5)))
    model.add(Dropout(0.05))

    model.add(Flatten())
    model.add(Dense(300, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(num_classes, activation='softmax'))

class YandexSansVsArialNetwork:
    def __init__(self, path2weights):
        self.__num_classes = 2
        self.__input_shape = (300, 300, 3)
