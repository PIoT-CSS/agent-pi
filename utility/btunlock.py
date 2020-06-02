"""
btunlock.py contains bluetooth car-unlocking feature for engineers.
"""
import bluetooth
import time
import threading

# engineers' MAC addresses
# TODO: RECEIVE THE LIST FROM MP?
ENGINEERS_BT_MAC_ADDRESSES = ['F0:99:B6:23:5F:4F']

# bluetooth scanning interval in seconds
BT_SCAN_INTERVAL_SECS = 1

# keyword to input to cancel the bluetooth unlock operation
CANCEL_KEYWORD_INPUT = 'Q'

class BluetoothUnlocker:
    """
    A class to unlock car with bluetooth for engineers.
    """

    def __init__(self):
        self.keep_running = True

    def input_to_cancel(self):
        """
        Detect if user has chosen to cancel the bluetooth unlock operation.
        """
        while self.keep_running:
            if input() == CANCEL_KEYWORD_INPUT:
                self.keep_running = False

    def search_and_unlock(self):
        """
        Search for engineer's Bluetooth device with MAC address and unlock car

        :return: wifi_access_point
        :rtype: bool
        """
        print("Locating engineer's Bluetooth device... Press '{}' to cancel."
            .format(CANCEL_KEYWORD_INPUT))
        while self.keep_running:
            # initialise and run thread to detect if user has chosen to cancel
            input_to_cancel_thread = threading.Thread(target=self.input_to_cancel)
            input_to_cancel_thread.start()
            # get a list of nearby bluetooth devices
            nearby_devices = bluetooth.discover_devices()
            if self.keep_running:
                for mac_address in nearby_devices:
                    # check each nearby bluetooth devices
                    # and match with engineer's list of bluetooth MAC addreses
                    if mac_address in ENGINEERS_BT_MAC_ADDRESSES:
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
