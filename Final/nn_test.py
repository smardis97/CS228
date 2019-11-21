import sys

sys.path.insert(0, '..')

import Leap
from pygame_window import PYGAME_WINDOW
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
    tup = (v[0], v[2])
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
    global window, k, test_data
    base = handle_vector(bone.prev_joint)
    adjust_scale(base)
    base = scale_point_to_range(base)
    tip = handle_vector(bone.next_joint)
    if bone_type == 0 or bone_type == 3:
        test_data[0, k] = bone.next_joint[0]
        test_data[0, k + 1] = bone.next_joint[1]
        test_data[0, k + 2] = bone.next_joint[2]
        k = k + 3
    adjust_scale(tip)
    tip = scale_point_to_range(tip)
    window.draw_black_line(base, tip, bone_type)


def adjust_scale(point):
    global x_min, x_max, y_min, y_max
    if point[0] < x_min:
        x_min = point[0]
    if point[0] > x_max:
        x_max = point[0]
    if point[1] < y_min:
        y_min = point[1]
    if point[1] > y_max:
        y_max = point[1]


def invert_y(point):
    new_point = (point[0], constants.PYGAME_WINDOW_DEPTH - point[1])
    return new_point


def scale_point_to_range(point):
    new_point = (
        scale_to_range(point[0], x_min, x_max, 0, constants.PYGAME_WINDOW_WIDTH),
        scale_to_range(point[1], y_min, y_max, 0, constants.PYGAME_WINDOW_DEPTH)
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
clf = pickle.load(open("{}{}".format(constants.DATA_PATH, constants.NN_CLASSIFIER_FILE), 'rb'))
test_data = np.zeros((1, 30), dtype='f')

x_min = 1000
x_max = -1000
y_min = 1000
y_max = -1000

controller = Leap.Controller()

i = 0
k = 0
while True:
    PYGAME_WINDOW.prepare(window)
    frame = controller.frame()
    if len(frame.hands) > 0:
        k = 0
        handle_frame(frame)
        test_data = center_data(test_data)
        predicted_class = clf.Predict(test_data)
        print predicted_class
    PYGAME_WINDOW.reveal()

