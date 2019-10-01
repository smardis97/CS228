import pickle
import numpy as np

gestureFile = open('userData/gesture.p', 'rb')
gestureData = pickle.load(gestureFile)
print gestureData.shape
