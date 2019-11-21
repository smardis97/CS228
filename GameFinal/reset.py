import pickle
import constants

dictionary = {}

pickle.dump(dictionary, open("{}{}".format(constants.DATA_PATH, constants.USER_DATABASE_FILE), 'wb'))
