import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import random


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
    pass

window = PYGAME_WINDOW()

print(window)

x, y = 400, 400

controller = Leap.Controller()

i = 0

while True:
    frame = controller.frame()
    if (len(frame.hands) > 0):
        print "hand detected " + str(i)
        i += 1
#     PYGAME_WINDOW.prepare(window)
#     window.draw_black_circle(x, y)
#     perturb_circle_position()
#     PYGAME_WINDOW.reveal()

