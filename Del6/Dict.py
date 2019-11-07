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
        database[user_name] = {"logins": 1}
        print 'welcome ' + user_name + '.'

    print database


def save():
    pickle.dump(database, open('Del6/userData/database.p', 'wb'))
