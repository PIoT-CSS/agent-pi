"""
btunlock.py contains bluetooth car-unlocking feature for engineers.
"""
import bluetooth
import time
import threading
import os
import json
from mqtt.publish import Publisher

# engineers' MAC addresses file
MAC_ADDR_FILE = "utility/mac_addresses.json"

# bluetooth scanning interval in seconds
BT_SCAN_INTERVAL_SECS = 1

# interval in secs for checking if MAC_ADDR_FILE exists
CHECK_MAC_ADDR_FILE_INTERVAL_SECS = 3

# keyword to input to cancel the bluetooth unlock operation
CANCEL_KEYWORD_INPUT = 'Q'

class BluetoothUnlocker:
    """
    A class to unlock car with bluetooth for engineers.
    """

    def __init__(self):
        self.keep_running = True

    def retrieve_mac_addresses(self):
        """
        Retrieve list of engineers' device's Bluetooth MAC address from file

        :return: list of engineers' device's Bluetooth MAC address
        :rtype: list
        """
        print("Receiving engineers' Bluetooth MAC addresses from MP...")
        while self.keep_running:
            # sleep to ensure payload has already be received
            time.sleep(CHECK_MAC_ADDR_FILE_INTERVAL_SECS)
            # check for existance of mac address file
            if os.path.exists(MAC_ADDR_FILE):
                with open(MAC_ADDR_FILE) as mac_address_file:
                    # load mac addresses from file
                    mac_addresses = json.load(mac_address_file)
                # get rid of the mac addresses file
                os.remove(MAC_ADDR_FILE)
                if len(mac_addresses['macAddresses']) == 0:
                    # don't run if there are no engineers registered on MP
                    print("Failed to fetch engineers' Bluetooth "
                        + "MAC addresses!")
                    return None
                else:
                    print("Received engineers' Bluetooth MAC addresses!")
                    return mac_addresses['macAddresses']
        return None

    def input_to_cancel(self):
        """
        Detect if user has chosen to cancel the bluetooth unlock operation.
        """
        while self.keep_running:
            if input() == CANCEL_KEYWORD_INPUT:
                print("Cancelling operation...")
                self.keep_running = False

    def search_and_unlock(self):
        """
        Search for engineer's Bluetooth device with MAC address and unlock car

        :return: wifi_access_point
        :rtype: bool
        """
        # initialise and run thread to detect if user has chosen to cancel
        input_to_cancel_thread = threading.Thread(target=self.input_to_cancel)
        input_to_cancel_thread.start()
        # obtain mac addresses from MP
        mac_addresses = self.retrieve_mac_addresses()
        if mac_addresses == None:
            return False
        print("Locating engineer's Bluetooth device... Press '{}' to cancel."
            .format(CANCEL_KEYWORD_INPUT))
        while self.keep_running:
            # get a list of nearby bluetooth devices
            nearby_devices = bluetooth.discover_devices()
            if self.keep_running:
                for mac_address in nearby_devices:
                    # check each nearby bluetooth devices
                    # and match with engineer's list of bluetooth MAC addreses
                    if mac_address in mac_addresses:
                        self.keep_running = False
                        print("Engineer's device found! Bluetooth MAC: {}"
                            .format(mac_address))
                        # to join input_to_cancel_thread
                        print("Press [enter] to unlock car.")
                        return True
                time.sleep(BT_SCAN_INTERVAL_SECS)
        return False


if __name__ == "__main__":
    BluetoothUnlocker().search_and_unlock()
