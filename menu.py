import sys

from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from auth.authenticate import Authenticator
from mqtt.publish import Publisher
from utility.geolocation import Geolocation
import datetime
import json

def action(name):

    if name == 'UserPass':
        print("\nAuthenticating {}\n".format(name))
        username = Screen().input('Enter in Username: ')
        password = Screen().input('Enter in Password: ')
        auth = Authenticator()
        auth.authenticate_user_pass(username, password)
    
    elif name == 'FaceRecog':
        print("\nAuthenticating with Face Recognition")
        username = Screen().input('Enter in Username: ')
        auth = Authenticator()
        if auth.authenticate_facialrecognition(username):
            Screen().input('Press [Enter] to continue, the car has been unlocked')
        else:
            Screen().input('Press [Enter] to continue, the car failed to unlock')

def main():
    # Change some menu formatting
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
    .set_prompt("SELECT>") \
    .set_title_align('center') \
    .set_subtitle_align('center') \
    .set_left_margin(4) \
    .set_right_margin(4) \
    .show_header_bottom_border(True)
    menu = ConsoleMenu("CarShare Application", "Welcome to CarShare, where you can rent a car and stuff...", formatter=menu_format)
    book_car = MenuItem("Book Car", menu)

    # Create a different formatter for another submenu, so it has a different look
    submenu_formatter = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.ASCII_BORDER)

    # Unlock Car Menu
    unlockcar_submenu = ConsoleMenu("Unlock Car", "Choose your method of authentication",
                formatter=submenu_formatter)

    unlock_pw= FunctionItem("Unlock the device with Username & Password ", action, args={"UserPass"}, should_exit=True)
    unlock_fr = FunctionItem("Unlock the device with Facial Recoginition", action, args={"FaceRecog"}, should_exit=True)
    unlockcar_submenu.append_item(unlock_pw)
    unlockcar_submenu.append_item(unlock_fr)

    # Return Car Menu
    returncar_submenu = ConsoleMenu("Return Car", "Return it")


    # Menu item for opening submenu 2
    submenu_item_1 = SubmenuItem("Unlock Car", submenu=unlockcar_submenu)
    submenu_item_2 = SubmenuItem("Return Car", submenu=returncar_submenu)
    submenu_item_1.set_menu(menu)
    submenu_item_2.set_menu(menu)

    # Add all the items to the root menu
    menu.append_item(submenu_item_1)
    menu.append_item(submenu_item_2)

    # Show the menu
    menu.show()

if __name__=="__main__":
    main()
