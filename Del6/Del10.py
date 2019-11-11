import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants
import pickle
import numpy as np
import Dict
import pygame
import time
import utility


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
    global window, k, testData
    base = bone.prev_joint
    adjust_scale(base)
    base = scale_to_top_left(base)
    tip = bone.next_joint
    if bone_type == 0 or bone_type == 3:
        testData[0, k] = bone.next_joint[0]
        testData[0, k+1] = bone.next_joint[1]
        testData[0, k+2] = bone.next_joint[2]
        k = k + 3
    adjust_scale(tip)
    tip = scale_to_top_left(tip)
    window.draw_black_line(base, tip, bone_type)


def adjust_scale(point):
    global xMin, xMax, yMin, yMax, zMin, zMax
    if point[0] < xMin:
        xMin = point[0]
    if point[0] > xMax:
        xMax = point[0]
    if point[1] < yMin:
        yMin = point[1]
    if point[1] > yMax:
        yMax = point[1]
    if point[2] < zMin:
        zMin = point[2]
    if point[2] > zMax:
        zMax = point[2]


def invert_y(point):
    new_point = (point[0], constants.pygameWindowHeight - point[1])
    return new_point


def scale_to_top_left(point):
    new_point = (
        utility.scale_to_range(point[0], xMin, xMax, 0, constants.pygameWindowWidth / 2),
        utility.scale_to_range(point[2], zMin, zMax, 0, constants.pygameWindowHeight / 2)
    )
    return new_point


def scale_to_top_right(point):
    new_point = (
        utility.scale_to_range(point[0], xMin, xMax, constants.pygameWindowWidth / 2, constants.pygameWindowWidth),
        utility.scale_to_range(point[2], zMin, zMax, 0, constants.pygameWindowHeight / 2)
    )
    return new_point


def scale_to_bottom_left(point):
    new_point = (
        utility.scale_to_range(point[0], xMin, xMax, 0, constants.pygameWindowWidth / 2),
        utility.scale_to_range(point[2], zMin, zMax, constants.pygameWindowHeight / 2, constants.pygameWindowHeight)
    )
    return new_point


def scale_to_bottom_right(point):
    new_point = (
        utility.scale_to_range(point[0], xMin, xMax, constants.pygameWindowWidth / 2, constants.pygameWindowWidth),
        utility.scale_to_range(point[2], zMin, zMax, constants.pygameWindowHeight / 2, constants.pygameWindowHeight)
    )
    return new_point


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
    if xMin + (x_range / 2) - (0.3 * x_range) > x_avg:
        lr_centering = -1
    elif xMin + (x_range / 2) + (0.3 * x_range) < x_avg:
        lr_centering = 1
    else:
        lr_centering = 0

    if yMin + (y_range / 2) - (0.3 * y_range) > y_avg:
        ud_centering = -1
    elif yMin + (y_range / 2) + (0.3 * y_range) < y_avg:
        ud_centering = 1
    else:
        ud_centering = 0
    return lr_centering, ud_centering


def level_up():
    global user
    if Dict.database[user]["level"] < 20:
        Dict.database[user]["level"] += 1
    set_round_length()


def set_round_length():
    global round_length, user
    round_length = 40 if Dict.database[user]["level"] <= 15 else 40 - 5 * (Dict.database[user]["level"] - 15)


window = PYGAME_WINDOW()
user = Dict.start_up()
Dict.check_user(user)
program_state = 0
clf = pickle.load(open('Del6/userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')
requested_class = None
previous_class = -1
correct_count = 0
start_time = time.time()
end_time = time.time()
round_length = 40
set_round_length()

xMin = 1000
xMax = -1000
yMin = 1000
yMax = -1000
zMin = 1000
zMax = -1000

x, y = 400, 400
pygameX, pygameY = 400, 400

controller = Leap.Controller()

i = 0
k = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Dict.save()
            exit(0)
    PYGAME_WINDOW.prepare(window)
    frame = controller.frame()
    if len(frame.hands) > 0:
        program_state = 1
        k = 0
        handle_frame(frame)
    else:
        program_state = 0
    if program_state == 0:
        window.draw_help_image()
    elif program_state == 1:
        if window.draw_help_image(True, determine_centering(frame.hands[0])):
            program_state = 2
    if program_state == 2:
        if time.time() - start_time <= round_length:
            if requested_class is None:
                requested_class = previous_class
                while requested_class == previous_class:
                    requested_class = random.randint(0, 9) if Dict.database[user]["level"] >= 10 else random.randint(0, Dict.database[user]["level"])
                if "attempts" + str(requested_class) not in Dict.database[user]:
                    Dict.database[user]["attempts" + str(requested_class)] = 1
                else:
                    Dict.database[user]["attempts" + str(requested_class)] += 1
                if "times" + str(requested_class) not in Dict.database[user]:
                    Dict.database[user]["times" + str(requested_class)] = []
                start_time = time.time()
            if requested_class is not None:
                window.draw_user_visualization(Dict.database[user], requested_class)
                if time.time() - start_time < round_length:
                    window.draw_example(requested_class, Dict.database[user]["level"])
                    testData = center_data(testData)
                    predicted_class = clf.Predict(testData)
                    if predicted_class == requested_class:
                        window.draw_help_visualization(True)
                        correct_count += 1
                    else:
                        window.draw_help_visualization(False)
                        correct_count = 0
                    if correct_count >= 10:
                        print "Success!"
                        end_time = time.time()
                        Dict.database[user]["times" + str(requested_class)].append(end_time - start_time)
                        Dict.database[user]["successes" + str(requested_class)] += 1
                        start_time = time.time()
                        end_time = time.time()
                        previous_class = requested_class
                        requested_class = None
                        correct_count = 0
                        moving_on = True
                        if Dict.database[user]["level"] < 5:
                            for i in range(Dict.database[user]["level"] + 1):
                                if Dict.database[user]["successes" + str(i)] < 5:
                                    moving_on = False
                                    break
                        elif Dict.database[user]["level"] < 10:
                            for i in range(Dict.database[user]["level"] + 1):
                                if Dict.database[user]["successes" + str(i)] < 10:
                                    moving_on = False
                                    break
                        elif Dict.database[user]["level"] < 15:
                            for i in range(10):
                                if Dict.database[user]["successes" + str(i)] < 15:
                                    moving_on = False
                                    break
                        else:
                            for i in range(10):
                                if Dict.database[user]["successes" + str(i)] < 15 + 3 * (Dict.database[user]["level"] - 15):
                                    moving_on = False
                        if moving_on:
                            level_up()
                        Dict.save()
        else:
            end_time = time.time()
            print "start: " + str(start_time)
            print "end: " + str(end_time)
            print "difference: " + str(end_time - start_time)
            print "result: ", end_time - start_time >= round_length
            print "--------------------------------------"
            previous_class = requested_class
            requested_class = None
            correct_count = 0
            start_time = time.time()
            end_time = time.time()

    window.draw_dividers()
    window.draw_secondary_dividers()
    window.draw_axes()
    window.draw_group_visualization(Dict.database, user)

    PYGAME_WINDOW.reveal()
