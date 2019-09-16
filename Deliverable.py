import sys

sys.path.insert(0, '..')

import Leap
from pygameWindow import PYGAME_WINDOW
import constants


class DELIVERABLE:
    def __init__(self):
        self.controller = Leap.Controller()
        self.pygameWindow = PYGAME_WINDOW()
        self.x = 400
        self.y = 400
        self.xMin = 1000
        self.xMax = -1000
        self.yMin = 1000
        self.yMax = -1000

    def handle_frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.handle_finger(finger)

    def handle_finger(self, finger):
        for b in range(4):
            self.handle_bone(finger.bone(b), b)

    def handle_bone(self, bone, bone_type):
        base = self.handle_vector(bone.prev_joint)
        self.adjust_scale(base)
        base = DELIVERABLE.invert_y(self.scale_point_to_range(base))
        tip = self.handle_vector(bone.next_joint)
        self.adjust_scale(tip)
        tip = DELIVERABLE.invert_y(self.scale_point_to_range(tip))
        self.pygameWindow.draw_bone(base, tip, bone_type)

    def adjust_scale(self, point):
        if point[0] < self.xMin:
            self.xMin = point[0]
        if point[0] > self.xMax:
            self.xMax = point[0]
        if point[1] < self.yMin:
            self.yMin = point[1]
        if point[1] > self.yMax:
            self.yMax = point[1]

    def scale_point_to_range(self, point):
        new_point = (
            DELIVERABLE.scale_to_range(point[0], self.xMin, self.xMax, 0, constants.pygameWindowWidth),
            DELIVERABLE.scale_to_range(point[1], self.yMin, self.yMax, 0, constants.pygameWindowHeight)
        )
        return new_point

    def run_forever(self):
        while True:
            self.pygameWindow.prepare(self.pygameWindow)
            frame = self.controller.frame()
            if len(frame.hands) > 0:
                self.handle_frame(frame)
            self.pygameWindow.reveal()

    @staticmethod
    def scale_to_range(val, init_min, init_max, final_min, final_max):
        init_range = init_max - init_min
        final_range = final_max - final_min
        if init_range == 0:
            new_val = final_min
        else:
            new_val = (((val - init_min) * final_range) / init_range) + final_min
        return int(new_val)

    @staticmethod
    def handle_vector(v):
        tup = (v[0], v[1])
        return tup

    @staticmethod
    def invert_y(point):
        new_point = (point[0], constants.pygameWindowHeight - point[1])
        return new_point
