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
    global window#, k, testData
    base = handle_vector(bone.prev_joint)
    adjust_scale(base)
    base = invert_y(scale_to_top_left(base))
    tip = handle_vector(bone.next_joint)
    # if bone_type == 0 or bone_type == 3:
    #     testData[0, k] = bone.next_joint[0]
    #     testData[0, k+1] = bone.next_joint[1]
    #     testData[0, k+2] = bone.next_joint[2]
    #     k = k + 3
    adjust_scale(tip)
    tip = invert_y(scale_to_top_left(tip))
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


def scale_to_bottom_left(point):
    new_point = (
        scale_to_range(point[0], xMin, xMax, 0, constants.pygameWindowWidth / 2),
        scale_to_range(point[1], yMin, yMax, 0, constants.pygameWindowHeight / 2)
    )
    return new_point


def scale_to_bottom_right(point):
    new_point = (
        scale_to_range(point[0], xMin, xMax, constants.pygameWindowWidth / 2, constants.pygameWindowWidth),
        scale_to_range(point[1], yMin, yMax, 0, constants.pygameWindowHeight / 2)
    )
    return new_point


def scale_to_top_left(point):
    new_point = (
        scale_to_range(point[0], xMin, xMax, 0, constants.pygameWindowWidth / 2),
        scale_to_range(point[1], yMin, yMax, constants.pygameWindowHeight / 2, constants.pygameWindowHeight)
    )
    return new_point


def scale_to_top_right(point):
    new_point = (
        scale_to_range(point[0], xMin, xMax, constants.pygameWindowWidth / 2, constants.pygameWindowWidth),
        scale_to_range(point[1], yMin, yMax, constants.pygameWindowHeight / 2, constants.pygameWindowHeight)
    )
    return new_point


def scale_to_range(val, init_min, init_max, final_min, final_max):
    init_range = init_max - init_min
    final_range = final_max - final_min
    if init_range == 0:
        new_val = final_min
    else:
        new_val = (((val - init_min) * final_range) / init_range) + final_min
    return int(new_val)


def determine_centering(hand):
    global xMin, xMax, yMin, yMax
    lr_centering = 0
    ud_centering = 0
    x_total = 0
    y_total = 0
    fingers = hand.fingers
    for finger in fingers:
        for b in range(4):
            bone = finger.bone(b)
            x_total += (bone.next_joint[0] + bone.prev_joint[0])
            y_total += (bone.next_joint[1] + bone.prev_joint[1])
    x_avg = x_total / 30
    y_avg = y_total / 30
    x_range = xMax - xMin
    y_range = yMax - yMin
    if xMin + (x_range / 2) - (0.2 * x_range) > x_avg:
        lr_centering = -1
    elif xMin + (x_range / 2) + (0.2 * x_range) < x_avg:
        lr_centering = 1
    else:
        lr_centering = 0

    if yMin + (y_range / 2) - (0.2 * y_range) > y_avg:
        ud_centering = -1
    elif yMin + (y_range / 2) + (0.2 * y_range) < y_avg:
        ud_centering = 1
    else:
        ud_centering = 0
    return lr_centering, ud_centering


window = PYGAME_WINDOW()
program_state = 0
# clf = pickle.load(open('Del6/userData/classifier.p', 'rb'))
# testData = np.zeros((1, 30), dtype='f')

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
        program_state = 1
        k = 0
        handle_frame(frame)
        # testData = center_data(testData)
        # predicted_class = clf.Predict(testData)
        # print predicted_class
    else:
        program_state = 0
    if program_state == 0:
        window.draw_help_image()
    elif program_state == 1:
        window.draw_help_image(True, determine_centering(frame.hands[0]))
    window.draw_dividers()

    PYGAME_WINDOW.reveal()

