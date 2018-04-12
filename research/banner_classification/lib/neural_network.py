from keras.layers import Input, Dense, Dropout, Flatten, MaxPooling2D
from keras.layers.convolutional import Conv2D
from keras.models import Model


def model_classify():
    input_shape = (100, 100, 3)
    input_img = Input(shape=input_shape)
    drop_prob = 0.5
    N_classes = 2

    x = Conv2D(3, (1, 1), padding='same', activation='relu')(input_img)

    x = Conv2D(16, (7, 7), activation='relu', padding='same')(x)
    x = Conv2D(16, (7, 7), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(64, (5, 5), activation='relu', padding='same')(x)
    x = Conv2D(64, (5, 5), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)

    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)

    flat = Flatten()(x)
    x = Dense(1000, activation='relu')(flat)
    x = Dropout(drop_prob)(x)

    x = Dense(300, activation='relu')(x)
    x = Dropout(drop_prob)(x)

    out = Dense(N_classes, activation='softmax')(x)
    model = Model(inputs=input_img, outputs=out)

    return model