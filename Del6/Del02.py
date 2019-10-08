import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants
import pickle
import numpy as np


def center_data(l):
    x_coords = l[0, ::3]
    y_coords = l[0, 1::3]
    z_coords = l[0, 2::3]
    x_mean = x_coords.mean()
    y_mean = y_coords.mean()
    z_mean = z_coords.mean()
    l[0, ::3] = x_coords - x_mean
    l[0, 1::3] = y_coords - y_mean
    l[0, 2::3] = z_coords - z_mean
    return l


def handle_vector(v):
    tup = (v[0], v[1])
    return tup


def handle_frame(frame):
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        handle_finger(finger)


def handle_finger(finger):
    for b in range(4):
        handle_bone(finger.bone(b), b)


def handle_bone(bone, bone_type):
    global window, k, testData
    base = handle_vector(bone.prev_joint)
    adjust_scale(base)
    base = invert_y(scale_point_to_range(base))
    tip = handle_vector(bone.next_joint)
    if bone_type == 0 or bone_type == 3:
        testData[0, k] = bone.next_joint[0]
        testData[0, k+1] = bone.next_joint[1]
        testData[0, k+2] = bone.next_joint[2]
        k = k + 3
    adjust_scale(tip)
    tip = invert_y(scale_point_to_range(tip))
    window.draw_black_line(base, tip, bone_type)


def adjust_scale(point):
    global xMin, xMax, yMin, yMax
    if point[0] < xMin:
        xMin = point[0]
    if point[0] > xMax:
        xMax = point[0]
    if point[1] < yMin:
        yMin = point[1]
    if point[1] > yMax:
        yMax = point[1]


def invert_y(point):
    new_point = (point[0], constants.pygameWindowHeight - point[1])
    return new_point


def scale_point_to_range(point):
    new_point = (
        scale_to_range(point[0], xMin, xMax, 0, constants.pygameWindowWidth),
        scale_to_range(point[1], yMin, yMax, 0, constants.pygameWindowHeight)
    )
    return new_point


def scale_to_range(val, init_min, init_max, final_min, final_max):
    init_range = init_max - init_min
    final_range = final_max -final_min
    if init_range == 0:
        new_val = final_min
    else:
        new_val = (((val - init_min) * final_range) / init_range) + final_min
    return int(new_val)

window = PYGAME_WINDOW()
clf = pickle.load(open('userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')

xMin = 1000
xMax = -1000
yMin = 1000
yMax = -1000

x, y = 400, 400
pygameX, pygameY = 400, 400

controller = Leap.Controller()

i = 0
k = 0
while True:
    PYGAME_WINDOW.prepare(window)
    frame = controller.frame()
    if len(frame.hands) > 0:
        k = 0
        handle_frame(frame)
        testData = center_data(testData)
        predicted_class = clf.Predict(testData)
        print predicted_class
    PYGAME_WINDOW.reveal()

