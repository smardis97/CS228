import constants
import dict
import graphics


def play(engine, gui, mstate):
    if engine.current_user is not None:
        engine.initialize_game()
    else:
        gui.state_change(constants.MENU_LOGIN)
        gui.set_error("MUST LOGIN")


def login(engine, gui, mstate):
    gui.state_change(constants.MENU_LOGIN)


def new_char(engine, gui, mstate):
    gui.state_change(constants.MENU_NEW_CHAR)


def text_confirm(engine, gui, mstate):
    if mstate == constants.MENU_LOGIN or mstate == constants.MENU_NEW_CHAR:
        name = ""
        for obj in gui.interactable:
            if type(obj) == graphics.TextBox:
                name = obj.text_content
                break
        if not dict.check_name(name):
            if mstate == constants.MENU_NEW_CHAR:
                dict.new_user(name)
            else:
                gui.set_error("USER NOT FOUND")
                return
        elif mstate == constants.MENU_NEW_CHAR:
            gui.set_error("USERNAME ALREADY TAKEN")
        engine.switch_users(name)
        gui.state_change(constants.MENU_MAIN)


def cancel(engine, gui, mstate):
    gui.state_change(constants.MENU_MAIN)


def settings(engine, gui, mstate):
    # gui.state_change(constants.MENU_SETTINGS)
    print "SETTINGS"


def quit_button(engine, gui, mstate):
    dict.save()
    exit(0)
