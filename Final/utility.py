import random


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
