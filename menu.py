"""
module for console menu. uses a library to format it.
"""
import sys

from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from auth.authenticate import Authenticator
from mqtt.publish import Publisher
from data.database import Database
from utility.geolocation import Geolocation
from utility.btunlock import BluetoothUnlocker
import datetime
import json


def action(name):
    """
    determines whether to use password or facial
    recognition for authenticating.
    """
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
            Screen().input("Waiting for camera to take picture")
    elif name == 'EngineerBT':
        #publish request to MP, requesting for engineers' Bluetooth MAC addr
        pub = Publisher()
        pub.publish("Requesting engineers' Bluetooth MAC addresses", 'MAC')
        if BluetoothUnlocker().search_and_unlock():
            auth = Authenticator()
            if auth.id_engineer():
                print("Engineer Identified, and \n")
                Screen().input('The car has been unlocked, '
                                + 'press [enter] to continue.')
            else:
                Screen().input('Failed to send Engineer Credentials, '
                                + 'press [enter] to continue.')
        else:
                Screen().input('The car failed to unlock, '
                            + 'press [enter] to continue.')
    elif name == 'Return':
        print("\nReturning the car")
        username = Screen().input('Enter in Username: ')
        now_time = datetime.datetime.now().isoformat()
        agent_id = Database().get_id()
        payload = {'username': username, 'timestamp': now_time,
                   'location': Geolocation().run(), 'agentid': agent_id}
        pub = Publisher()
        pub.publish(payload, 'RETURN')


def main():
    """
    contains logic for the console menu.
    """
    # Change some menu formatting
    menu_format = MenuFormatBuilder() \
        .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
        .set_prompt("SELECT>") \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)
    menu = ConsoleMenu("CarShare Application",
                       "Welcome to CarShare, " +
                       "where you can rent a car and stuff...",
                       formatter=menu_format)
    book_car = MenuItem("Book Car", menu)

    # Create a different formatter for another submenu,
    # so it has a different look
    submenu_formatter = MenuFormatBuilder().set_border_style_type(
        MenuBorderStyleType.ASCII_BORDER)

    # Unlock Car Menu
    unlockcar_submenu = ConsoleMenu("Unlock Car",
                                    "Choose your method of authentication",
                                    formatter=submenu_formatter)

    unlock_pw = FunctionItem("Unlock the device with Username & Password ",
                             action, args={"UserPass"}, should_exit=True)
    unlock_fr = FunctionItem("Unlock the device with Facial Recoginition",
                             action, args={
                                 "FaceRecog"}, should_exit=True)
    unlock_engineer_bt = FunctionItem("Unlock with engineer's Bluetooth device",
                                      action, args={"EngineerBT"}, should_exit=True)
    unlockcar_submenu.append_item(unlock_pw)
    unlockcar_submenu.append_item(unlock_fr)
    unlockcar_submenu.append_item(unlock_engineer_bt)

    # Return Car Menu
    returncar_submenu = ConsoleMenu("Return Car", "Return it")
    returncar = FunctionItem("Return the car", action, args={
                             "Return"}, should_exit=True)
    returncar_submenu.append_item(returncar)

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting CarShare Application...")
