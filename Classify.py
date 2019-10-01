import pickle
import numpy as np
from knn import KNN


def reshape_data(set1, set2):
    X = np.zeros((2000, 5*4*6), dtype='f')
    y = np.zeros(2000, dtype='f')
    for row in range(1000):
        y[row] = 7
        y[row+1000] = 8
        col = 0
        for finger in range(0, 5):
            for bone in range(0, 4):
                for point in range(0, 6):
                    X[row, col] = set1[finger, bone, point, row]
                    X[row+1000, col] = set2[finger, bone, point, row]
                    col += 1
    return X, y


def reduce_data(X):
    return X

knn = KNN()
knn.Use_K_Of(15)
train7 = reduce_data(pickle.load(open('userData/train7.dat')))
train8 = reduce_data(pickle.load(open('userData/train8.dat')))
test7 = reduce_data(pickle.load(open('userData/test7.dat')))
test8 = reduce_data(pickle.load(open('userData/test8.dat')))

trainX, trainy = reshape_data(train7, train8)
testX, testy = reshape_data(test7, test8)

knn.Fit(trainX, trainy)

predict_count = 0

for row in range(2000):
    prediction = knn.Predict(testX[row])
    if prediction == testy[row]:
        predict_count += 1

print float(predict_count) / 2000.


