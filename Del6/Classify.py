import pickle
import numpy as np
from knn import KNN


def reshape_data(tup_of_sets):
    X = np.zeros((len(tup_of_sets) * 1000, 5*2*3), dtype='f')
    y = np.zeros(len(tup_of_sets) * 1000, dtype='f')
    for row in range(1000):
        y[row] = 0
        y[row+1000] = 1
        y[row+2000] = 2
        y[row+3000] = 3
        y[row+4000] = 4
        y[row+5000] = 5
        y[row+6000] = 6
        y[row+7000] = 7
        y[row+8000] = 8
        y[row+9000] = 9
        col = 0
        for finger in range(0, 5):
            for bone in range(0, 2):
                for point in range(0, 3):
                    for i in range(0, len(tup_of_sets)):
                        X[row + (i * 1000), col] = tup_of_sets[i][finger, bone, point, row]
                    col += 1
    return X, y


def reduce_data(X):
    X = np.delete(X, 1, 1)
    X = np.delete(X, 1, 1)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    X = np.delete(X, 0, 2)
    return X


def center_data(X):
    allXCoordinates = X[:, :, 0, :]
    meanValue = allXCoordinates.mean()
    X[:, :, 0, :] = allXCoordinates - meanValue
    allYCoordinates = X[:, :, 1, :]
    meanValue = allYCoordinates.mean()
    X[:, :, 1, :] = allYCoordinates - meanValue
    allZCoordinates = X[:, :, 2, :]
    meanValue = allZCoordinates.mean()
    X[:, :, 2, :] = allZCoordinates - meanValue
    return X

knn = KNN()
knn.Use_K_Of(15)

train0 = center_data(reduce_data(pickle.load(open('Del6/userData/Clark_train0.p', 'rb'))))
test0 = center_data(reduce_data(pickle.load(open('Del6/userData/Clark_test0.p', 'rb'))))

train1 = center_data(reduce_data(pickle.load(open('Del6/userData/Newton_train1.p', 'rb'))))
test1 = center_data(reduce_data(pickle.load(open('Del6/userData/Newton_test1.p', 'rb'))))

train2 = center_data(reduce_data(pickle.load(open('Del6/userData/Apple_train2.p', 'rb'))))
test2 = center_data(reduce_data(pickle.load(open('Del6/userData/Apple_test2.p', 'rb'))))

train3 = center_data(reduce_data(pickle.load(open('Del6/userData/Apple_train3.p', 'rb'))))
test3 = center_data(reduce_data(pickle.load(open('Del6/userData/Apple_test3.p', 'rb'))))

train4 = center_data(reduce_data(pickle.load(open('Del6/userData/Deluca_train4.p', 'rb'))))
test4 = center_data(reduce_data(pickle.load(open('Del6/userData/Deluca_test4.p', 'rb'))))

train5 = center_data(reduce_data(pickle.load(open('Del6/userData/Deluca_train5.p', 'rb'))))
test5 = center_data(reduce_data(pickle.load(open('Del6/userData/Deluca_test5.p', 'rb'))))

train6 = center_data(reduce_data(pickle.load(open('Del6/userData/Boland_train6.p', 'rb'))))
test6 = center_data(reduce_data(pickle.load(open('Del6/userData/Boland_test6.p', 'rb'))))

train7 = center_data(reduce_data(pickle.load(open('Del6/userData/Erickson_train7.p', 'rb'))))
test7 = center_data(reduce_data(pickle.load(open('Del6/userData/Erickson_test7.p', 'rb'))))

train8 = center_data(reduce_data(pickle.load(open('Del6/userData/Erickson_train8.p', 'rb'))))
test8 = center_data(reduce_data(pickle.load(open('Del6/userData/Erickson_test8.p', 'rb'))))

train9 = center_data(reduce_data(pickle.load(open('Del6/userData/Lee_train9.p', 'rb'))))
test9 = center_data(reduce_data(pickle.load(open('Del6/userData/Lee_test9.p', 'rb'))))

num_symbols = 10

trainX, trainy = reshape_data((train0, train1, train2, train3, train4, train5, train6, train7, train8, train9))
testX, testy = reshape_data((test0, test1, test2, test3, test4, test5, test6, test7, test8, test9))

knn.Fit(trainX, trainy)

predict_count = 0

for row in range(num_symbols * 1000):
    prediction = knn.Predict(testX[row])
    if prediction == testy[row]:
        predict_count += 1

print 100 * (float(predict_count) / (num_symbols * 1000.))

pickle.dump(knn, open('Del6/userData/classifier.p', 'wb'))
