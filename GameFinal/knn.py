import numpy as np

import csv, operator, random

class KNN:

    def __init__(self):

        self.trainingSet=[]
        self.testSet=[]
        self.split = 0.67

        self.data = None
        self.target = None

        self.k = 1

        self.trainX = None

        self.trainy = None

    def Fit(self,trainX,trainy):

        self.trainX = trainX

        self.trainY = trainy

    # The Faster Predict Function
    #   modified by Sida Liu (sliu1), 2019/09/24
    # testFeatures can be in shape (2000, 30) or shape (30,)
    def Predict(self, testFeatures):
        # if there's only one testFeature
        if (len(testFeatures.shape)==1):
            # expand it to be 2-dims form: (n, 30), pretend there are multiple testFeatures.
            testFeatures = np.expand_dims(testFeatures, 0)

        predictions = []
        # iterate through each testFeatures
        for i in range(testFeatures.shape[0]):
            # use the broadcasting of numpy array, get 2000 distances of 30 dims features. 
            # (Broadcasting: while doing b-a, where b in shape (30,), a in shape (2000,30), numpy will automatically broadcast b to (2000,30) to match a, and get an answer of shape (2000,30))
            # shape of `v` is (2000, 30)
            v = testFeatures[i,:] - self.trainX
            # calculate euclidean distance for those 2000 distances
            # shape of `dist` is (2000,), since we choose keepdims=False, it has been flattened.
            dist = np.linalg.norm(v, axis=1, keepdims=False)
            # sort distances, find shortest k neighbors
            first_k_neighbor_index = np.argsort(dist)[:self.k]
            # check trainY for answers
            neighbors = self.trainY[first_k_neighbor_index]
            # count the answers, give the final answer
            prediction = np.argmax(np.bincount(neighbors.astype(dtype='int64')))
            # save final answer to a list
            predictions.append(prediction)
        # before return, convert list back to np.array, so users will be easier to compare with their testY
        return np.array(predictions)

    def Use_K_Of(self,k):

        self.k = k
