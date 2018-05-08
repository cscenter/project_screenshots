import random


def train_test_split(X, y, percentage=0.5):
    data_size = len(y)
    k = int(data_size * percentage)
    rand_int = list(range(data_size))
    random.shuffle(rand_int)

    X_train = X[rand_int[:-k]]
    y_train = y[rand_int[:-k]]
    X_test = X[rand_int[-k:]]
    y_test = y[rand_int[-k:]]

    return X_train, X_test, y_train, y_test
