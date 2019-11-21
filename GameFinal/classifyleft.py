import pickle
import numpy as np
from knn import KNN
import constants


def reshape(tup_of_sets):
    X = np.zeros((len(tup_of_sets) * 1000, 5*2*3), dtype='f')
    y = np.zeros(len(tup_of_sets) * 1000, dtype='f')
    for row in range(1000):
        y[row] = 0
        y[row+1000] = 1
        y[row+2000] = 2
        # y[row+3000] = 3
        y[row+3000] = 4
        y[row+4000] = 5
        # y[row+6000] = 6
        # y[row+7000] = 7
        # y[row+8000] = 8
        # y[row+9000] = 9
        col = 0
        for finger in range(0, 5):
            for bone in range(0, 2):
                for point in range(0, 3):
                    for i in range(0, len(tup_of_sets)):
                        X[row + (i * 1000), col] = tup_of_sets[i][finger, bone, point, row]
                    col += 1
    return X, y


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


def mirror_x(X):
    all_x_coordinates = X[:, :, 0, :]
    X[:, :, 0, :] = -1 * all_x_coordinates
    return X

knn = KNN()
knn.Use_K_Of(15)

train0 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_0_FILE), 'rb')))))
test0 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_0_FILE), 'rb')))))

train1 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_1_FILE), 'rb')))))
test1 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_1_FILE), 'rb')))))

train2 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_2_LEFT), 'rb')))))
test2 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_2_LEFT), 'rb')))))

# train3 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_3_LEFT), 'rb')))))
# test3 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_3_LEFT), 'rb')))))
#
train4 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_4_FILE), 'rb')))))
test4 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_4_FILE), 'rb')))))
#
train5 = center(reduce(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_5_LEFT), 'rb'))))
test5 = center(reduce(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_5_LEFT), 'rb'))))
#
# train6 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_6_FILE), 'rb')))))
# test6 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_6_FILE), 'rb')))))
#
# train7 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_7_FILE), 'rb')))))
# test7 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_7_FILE), 'rb')))))
#
# train8 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_8_LEFT), 'rb')))))
# test8 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_8_LEFT), 'rb')))))
#
# train9 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TRAIN_9_FILE), 'rb')))))
# test9 = center(reduce(mirror_x(pickle.load(open("{}{}".format(constants.DATA_PATH, constants.TEST_9_FILE), 'rb')))))

num_symbols = 5

trainX, trainy = reshape((train0, train1, train2, train4, train5))#, train6))#, train7))#, train8))#, train9))
testX, testy = reshape((test0, test1, test2, test4, test5))#, test6))#, test7))#, test8))#, test9))

knn.Fit(trainX, trainy)

predict_count = 0

for row in range(num_symbols * 1000):
    prediction = knn.Predict(testX[row])
    if prediction == testy[row]:
        predict_count += 1

print 100 * (float(predict_count) / (num_symbols * 1000.))

pickle.dump(knn, open("{}{}".format(constants.DATA_PATH, constants.NN_CLASSIFIER_FILE + "left"), 'wb'))
