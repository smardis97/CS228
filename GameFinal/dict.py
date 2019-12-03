import pickle
from constants import LOGIN_KEY, ATTEMPTS_KEY, SUCCESSES_KEY
import constants

database = {}


def start_up():
    global database
    database = pickle.load(open("{}{}".format(constants.DATA_PATH, constants.USER_DATABASE_FILE), 'rb'))


def check_name(user_name):
    return user_name in database


def login(user_name):
    if check_name(user_name):
        database[user_name][LOGIN_KEY] += 1
        return user_name
    else:
        return None


def new_user(user_name):
    if not check_name(user_name):
        database[user_name] = {
            LOGIN_KEY: 1,
            ATTEMPTS_KEY[0]: 0,
            SUCCESSES_KEY[0]: 0,
            ATTEMPTS_KEY[1]: 0,
            SUCCESSES_KEY[1]: 0,
            ATTEMPTS_KEY[2]: 0,
            SUCCESSES_KEY[2]: 0,
            ATTEMPTS_KEY[3]: 0,
            SUCCESSES_KEY[3]: 0,
            ATTEMPTS_KEY[4]: 0,
            SUCCESSES_KEY[4]: 0,
            ATTEMPTS_KEY[5]: 0,
            SUCCESSES_KEY[5]: 0,
            ATTEMPTS_KEY[6]: 0,
            SUCCESSES_KEY[6]: 0,
            ATTEMPTS_KEY[7]: 0,
            SUCCESSES_KEY[7]: 0,
            ATTEMPTS_KEY[8]: 0,
            SUCCESSES_KEY[8]: 0,
            ATTEMPTS_KEY[9]: 0,
            SUCCESSES_KEY[9]: 0,
        }
    return user_name


def auto_login(user_name):
    if user_name in database:
        database[user_name][LOGIN_KEY] += 1
        print 'welcome back ' + user_name + '.'
    else:
        database[user_name] = {
            LOGIN_KEY: 1,
            ATTEMPTS_KEY[0]: 0,
            SUCCESSES_KEY[0]: 0,
            ATTEMPTS_KEY[1]: 0,
            SUCCESSES_KEY[1]: 0,
            ATTEMPTS_KEY[2]: 0,
            SUCCESSES_KEY[2]: 0,
            ATTEMPTS_KEY[3]: 0,
            SUCCESSES_KEY[3]: 0,
            ATTEMPTS_KEY[4]: 0,
            SUCCESSES_KEY[4]: 0,
            ATTEMPTS_KEY[5]: 0,
            SUCCESSES_KEY[5]: 0,
            ATTEMPTS_KEY[6]: 0,
            SUCCESSES_KEY[6]: 0,
            ATTEMPTS_KEY[7]: 0,
            SUCCESSES_KEY[7]: 0,
            ATTEMPTS_KEY[8]: 0,
            SUCCESSES_KEY[8]: 0,
            ATTEMPTS_KEY[9]: 0,
            SUCCESSES_KEY[9]: 0,
        }
        print 'welcome ' + user_name + '.'

    print database


def save():
    pickle.dump(database, open("{}{}".format(constants.DATA_PATH, constants.USER_DATABASE_FILE), 'wb'))
