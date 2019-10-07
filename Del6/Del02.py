import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants


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
    global window
    base = handle_vector(bone.prev_joint)
    adjust_scale(base)
    base = invert_y(scale_point_to_range(base))
    tip = handle_vector(bone.next_joint)
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

xMin = 1000
xMax = -1000
yMin = 1000
yMax = -1000

x, y = 400, 400
pygameX, pygameY = 400, 400

controller = Leap.Controller()

i = 0

while True:
    PYGAME_WINDOW.prepare(window)
    frame = controller.frame()
    if len(frame.hands) > 0:
        handle_frame(frame)
        # pygameX = scale_to_range(x, xMin, xMax, 0, constants.pygameWindowWidth)
        # pygameY = constants.pygameWindowHeight - scale_to_range(y, yMin, yMax, 0, constants.pygameWindowHeight)
    #     print 'Coords: (' + str(pygameX) + ', ' + str(pygameY) + ')'
    # window.draw_black_circle(pygameX, pygameY)
    PYGAME_WINDOW.reveal()

