import random
import math
import constants


def scale_to_range(val, init_min, init_max, final_min, final_max):
    init_range = init_max - init_min
    final_range = final_max - final_min
    if init_range == 0:
        new_val = final_min
    else:
        new_val = (((val - init_min) * final_range) / init_range) + final_min
    return int(new_val)


def randomize_arithmetic(target):
    sign_picker = ['+', '-']
    sign = sign_picker[random.randint(0, 1)]
    first_val = 0
    second_val = 0
    if sign == '+':
        if target != 0:
            first_val = random.randint(0, target - 1)
            second_val = target - first_val
        else:
            pass
    else:
        first_val = random.randint(target, 20)
        second_val = first_val - target

    return first_val, sign, second_val


def get_vector(heading, magnitude):
    return magnitude * math.cos(math.radians(heading)), magnitude * math.sin(math.radians(heading))


def vector_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


def get_next(obj, li):
    return li[(li.index(obj) + 1) % len(li)]


def polar_to_cartesian(v):
    angle = v[0] % constants.CIRCLE_DEG
    x_val = v[1] * math.cos(math.radians(angle))
    y_val = v[1] * math.sin(math.radians(angle))
    return x_val, y_val


def cartesian_to_polar(v):
    angle = math.degrees(math.atan(v[1]/v[0]))
    magnitude = math.sqrt(v[0]**2 + v[1]**2)
    return angle, magnitude


def tuple_float_to_int(v):
    return int(v[0]), int(v[1])
