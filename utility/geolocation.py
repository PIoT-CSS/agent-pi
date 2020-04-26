"""
WifiObject.py module, task is to scan Wifi and return Mac Addresses
in json format to be used by Google Geolocation API
"""

import re
import subprocess
import requests

# define string for regex pattern
NEW_LINE = "\n"
CELL = "Cell"
UNKNOWN = "Unknown"

# define regex pattern for Mac Address
MAC_ADDRESS_PATTERN = re.compile(r'(?:[0-9a-fA-F]:?){12}')
NUMBER_PATTERN = re.compile(r'\d+')

# define array for wifi scanning unix command
WIFI_SCAN_COMMAND = ["sudo", "iwlist", "scanning"] #! apt-get -y install wireless-tools

# define url for google geolocation api
GOOGLE_GEO_API_URL = 'https://www.googleapis.com/geolocation/v1/geolocate?key='
GOOGLE_KEY = 'AIzaSyDeUow5kbHYOmzrm4C3SoyIml16O8CZtkA'

class Geolocation:
    """
    A class to Scan wifi


    Methods
    -------
    scan_wifi_information(self):
        Uses the command "sudo iwlist scanning" to scan for wifi
    format_list(self, scan_result):
        Splits scan result into 2d array and filters non human readable string
    convert_to_json(self, information_list):
        Takes in list of wifi information, perform regex operations to extract 
        Mac address, channel, signal strength and return a json object
    make_request_to_google_geo_api(self, payload): 
        Send payload to google geolocation api and returns a json response  
    -------
    """

    def scan_wifi_information(self):
        """
        Uses the command "sudo iwlist scanning" to scan for wifi
        """
        results = subprocess.check_output(WIFI_SCAN_COMMAND)

        results = results.decode("utf-8") # needed in python 3

        return results

    def format_list(self, scan_result):
        """
        Splits scan result into 2d array and filters not human readable string
        """
        split_result = scan_result.split(CELL)
        split_result = split_result[1:]
        wifi_list = []

        for wifi in split_result:
            wifi_information = wifi.split(NEW_LINE)
            wifi_information = [i for i in wifi_information if not re.search(UNKNOWN, i)]
            wifi_list.append(wifi_information)

        return wifi_list

    def convert_to_json(self, information_list):
        """
        Takes in list of wifi information, perform regex operations to extract 
        Mac address, channel, signal strenght and return a json object
        """
        mac_address = re.findall(MAC_ADDRESS_PATTERN, information_list[0])[0]
        channel = re.findall(NUMBER_PATTERN, information_list[1])[0]
        signal_strength = re.findall(NUMBER_PATTERN, information_list[3])[2]

        wifi_access_point = {
            'macAddress': mac_address,
            'channel': channel,
            'signalStrength': signal_strength
        }

        return wifi_access_point

    def make_request_to_google_geo_api(self, payload):
        """
        Send payload to google geolocation api and returns json
        """
        url = GOOGLE_GEO_API_URL + GOOGLE_KEY
        request = requests.post(url, json=payload)
        print(request.json())

        return request.json()

    def run(self):
        """
        Init and runs ScanWifi
        """
        wifi_list = self.scan_wifi_information()
        formatted_list = self.format_list(wifi_list)
        payload = {"wifiAccessPoints": []}

        for i in formatted_list:
            payload['wifiAccessPoints'].append(self.convert_to_json(i))

        self.make_request_to_google_geo_api(payload)


if __name__ == "__main__":
    Geolocation().run()
