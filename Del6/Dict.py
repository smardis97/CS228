import pickle

database = {}


def start_up():
    global database
    database = pickle.load(open('Del6/userData/database.p', 'rb'))

    user_name = raw_input('Please enter your name: ')
    return user_name


def check_user(user_name):
    if user_name in database:
        database[user_name]["logins"] += 1
        print 'welcome back ' + user_name + '.'
    else:
        database[user_name] = {
            "logins": 1,
            "level": 1,
            "attempts0": 0,
            "successes0": 0,
            "times0": [],
            "attempts1": 0,
            "successes1": 0,
            "times1": [],
            "attempts2": 0,
            "successes2": 0,
            "times2": [],
            "attempts3": 0,
            "successes3": 0,
            "times3": [],
            "attempts4": 0,
            "successes4": 0,
            "times4": [],
            "attempts5": 0,
            "successes5": 0,
            "times5": [],
            "attempts6": 0,
            "successes6": 0,
            "times6": [],
            "attempts7": 0,
            "successes7": 0,
            "times7": [],
            "attempts8": 0,
            "successes8": 0,
            "times8": [],
            "attempts9": 0,
            "successes9": 0,
            "times9": [],
        }
        print 'welcome ' + user_name + '.'

    print database


def save():
    pickle.dump(database, open('Del6/userData/database.p', 'wb'))
