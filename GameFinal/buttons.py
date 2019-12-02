import constants


def play(engine, gui, mstate):
    engine.initialize_game()


def login(engine, gui, mstate):
    gui.state_change(constants.MENU_LOGIN)


def new_char(engine, gui, mstate):
    gui.state_change(constants.MENU_NEW_CHAR)


def text_confirm(engine, gui, mstate):
    print "CONFIRM"


def cancel(engine, gui, mstate):
    gui.state_change(constants.MENU_MAIN)


def settings(engine, gui, mstate):
    print "SETTINGS"


def quit_button(engine, gui, mstate):
    exit(0)
