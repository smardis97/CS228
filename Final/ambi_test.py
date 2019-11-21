import constants
import pickle
import numpy as np


def reduce(X):
    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    return X


def center(X):
    all_x_coordinates = X[:, :, 0, :]
    mean_value = all_x_coordinates.mean()
    X[:, :, 0, :] = all_x_coordinates - mean_value
    all_y_coordinates = X[:, :, 1, :]
    mean_value = all_y_coordinates.mean()
    X[:, :, 1, :] = all_y_coordinates - mean_value
    all_z_coordinates = X[:, :, 2, :]
    mean_value = all_z_coordinates.mean()
    X[:, :, 2, :] = all_z_coordinates - mean_value
    return X

train5 = pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_5_FILE), 'rb'))
test5 = pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_5_FILE), 'rb'))

print train5.shape
