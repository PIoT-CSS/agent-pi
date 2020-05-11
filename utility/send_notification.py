"""
send_notification.py module, task is to send a .txt file to notify
lock/unlock through bluetooth with a device that was already paired using a script.
"""
import subprocess
import pathlib
import os

CURRENT_WORKING_DIR = pathlib.Path().absolute().as_posix()

class SendNotification:
    """
    A class that runs a script that sends file to a device.
    """

    def run(self, mac_address, file):
        """
        Takes in the bluetooth mac_address of a device and file,
        and runs a script with these two values as arguments.
        """
        
        run_script = ["expect", "obex_send_file.sh"]
        file_path = CURRENT_WORKING_DIR + os.sep + file

        run_script.append(mac_address)
        run_script.append(file_path)
        
        results = subprocess.check_output(run_script)

        print(results)

if __name__ == "__main__":
    SendNotification().run("40:4E:36:9E:DD:8E", "car_unlocked.jpg")

