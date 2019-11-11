import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import random
import constants


def perturb_circle_position():
    global x, y
    die_roll = random.randint(1, 4)
    if die_roll == 1:
        x += 1
    elif die_roll == 2:
        x -= 1
    elif die_roll == 3:
        y += 1
    else:
        y -= 1


def handle_frame(frame):
    global x, y, x_min, x_max, y_min, y_max
    hand = frame.hands[0]
    indexFinger = hand.fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
    distalPhalanx = indexFinger.bone(3)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[1])
    if (x < xMin):
        xMin = x
    if (x > xMax):
        xMax = x
    if (y < yMin):
        yMin = y
    if (y > yMax):
        yMax = y
    print '(x, y): (' + str(x) + ', ' + str(y) + ')'
    print 'X limits: (' + str(xMin) + ', ' + str(xMax) + ')'
    print 'Y limits: (' + str(yMin) + ', ' + str(yMax) + ')'


def scale_to_range(val, init_min, init_max, final_min, final_max):
    init_range = init_max - init_min
    final_range = final_max -final_min
    if init_range == 0:
        new_val = final_min
    else:
        new_val = (((val - init_min) * final_range) / init_range) + final_min
    return int(new_val)

window = PYGAME_WINDOW()

print(window)

x_min = 1000
x_max = -1000
y_min = 1000
y_max = -1000

x, y = 400, 400
pygameX, pygameY = 400, 400

controller = Leap.Controller()

i = 0

while True:
    PYGAME_WINDOW.prepare(window)
    frame = controller.frame()
    if (len(frame.hands) > 0):
        handle_frame(frame)
        pygameX = scale_to_range(x, x_min, x_max, 0, constants.PYGAME_WINDOW_WIDTH)
        pygameY = constants.PYGAME_WINDOW_DEPTH - scale_to_range(y, y_min, y_max, 0, constants.PYGAME_WINDOW_DEPTH)
        print 'Coords: (' + str(pygameX) + ', ' + str(pygameY) + ')'
    window.draw_black_circle(pygameX, pygameY)
    PYGAME_WINDOW.reveal()

