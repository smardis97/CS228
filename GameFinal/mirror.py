import os
import constants
import pickle


def mirror_x(X):
    all_x_coordinates = X[:, :, 0, :]
    X[:, :, 0, :] = -1 * all_x_coordinates
    return X


for f in os.listdir(constants.DATA_PATH):
    if f.endswith("0.p") or f.endswith("1.p") or f.endswith("2.p") or f.endswith("3.p") or f.endswith("4.p")\
            or f.endswith("5.p") or f.endswith("6.p") or f.endswith("7.p") or f.endswith("8.p") or f.endswith("9.p"):
        try:
            print f
            right_data = pickle.load(open("{}{}".format(constants.DATA_PATH, f), "rb"))
            left_data = mirror_x(right_data)
            pickle.dump(left_data, open("{}{}_left.p".format(constants.DATA_PATH, f[:-2]), "wb"))
        except KeyError:
            continue
        except ImportError:
            continue
        except IndexError:
            continue
