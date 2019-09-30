from knn import KNN
import matplotlib.pyplot as plt
import numpy as np

knn = KNN()
knn.Load_Dataset('iris.csv')

trainX = knn.data[::2, 1:3]
trainy = knn.target[::2]
testX = knn.data[1::2, 1:3]
testy = knn.target[1::2]
colors = np.zeros((3, 3), dtype='f')
colors[0, :] = [1, 0.5, 0.5]
colors[1, :] = [0.5, 1, 0.5]
colors[2, :] = [0.5, 0.5, 1]
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)
plt.figure()
[numItems, numFeatures] = knn.data.shape
for i in range(0, numItems/2):
    itemClass = int(trainy[i])
    currColor = colors[itemClass, :]
    plt.scatter(trainX[i, 0], trainX[i, 1], facecolor=currColor, edgecolor=[0, 0, 0], s=50, lw=2)
count = 0
for i in range(0, numItems/2):
    itemClass = int(testy[i])
    actColor = colors[itemClass, :]
    prediction = knn.Predict(testX[i, 0:2])
    predColor = colors[prediction, :]
    if itemClass == prediction:
        count += 1
    plt.scatter(testX[i, 0], testX[i, 1], facecolor=actColor, edgecolor=predColor, s=50, lw=2)
rat = (float(count) / float(numItems/2)) * 100
print rat
plt.show()
