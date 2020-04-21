"""
WifiObject.py module, task is to scan Wifi and return Mac Addresses
in json format to be used by Google Geolocation API
"""

import sys
import re
import subprocess
import time
import json
import requests

# define string for regex pattern
NEW_LINE = "\n"
CELL = "Cell"
UNKNOWN = "Unknown"

# define regex pattern for Mac Address
MAC_ADDRESS_PATTERN = re.compile(r'(?:[0-9a-fA-F]:?){12}')
NUMBER_PATTERN = re.compile('\d+')

# define array for wifi scanning unix command
WIFI_SCAN_COMMAND = ["sudo","iwlist","scanning"] #! apt-get -y install wireless-tools

# define url for google geolocation api
GOOGLE_GEO_API_URL = 'https://www.googleapis.com/geolocation/v1/geolocate?key='
GOOGLE_KEY = 'AIzaSyDeUow5kbHYOmzrm4C3SoyIml16O8CZtkA'

class Geolocation:
    """
    A class to Scan wifi


    Methods
    -------
    scanWifiInformation(self):
        Uses the command "sudo iwlist scanning" to scan for wifi
    formatList(self, scanResult):
        Splits scan result into 2d array and filters non human readable string
    convertToJson(self, informationList):
        Takes in list of wifi information, perform regex operations to extract 
        Mac address, channel, signal strength and return a json object
    makeRequestToGoogleGeoApi(self, payload): 
        Send payload to google geolocation api and returns a json response  
    -------
    """
    
    def scanWifiInformation(self):
        """
        Uses the command "sudo iwlist scanning" to scan for wifi
        """
        results = subprocess.check_output(WIFI_SCAN_COMMAND)
         
        results = results.decode("utf-8") # needed in python 3
        
        return results

    def formatList(self, scanResult):
        """
        Splits scan result into 2d array and filters not human readable string
        """
        ls = scanResult.split(CELL)
        ls = ls[1:]
        wifiList = []
        
        for l in ls:
            wifiInfomration = l.split(NEW_LINE)
            wifiInfomration = [i for i in wifiInfomration if not re.search(UNKNOWN, i)]
            wifiList.append(wifiInfomration)
        
        return wifiList
    
    def convertToJson(self, informationList):
        """
        Takes in list of wifi information, perform regex operations to extract 
        Mac address, channel, signal strenght and return a json object
        """
        macAddress = re.findall(MAC_ADDRESS_PATTERN, informationList[0])[0]
        channel = re.findall(NUMBER_PATTERN, informationList[1])[0]
        signalStrength = re.findall(NUMBER_PATTERN, informationList[3])[2]
        age = time.time()

        wifiAccessPoint = {
            'macAddress': macAddress,
            'channel': channel,
            'signalStrength': signalStrength
            }

        return wifiAccessPoint
    
    def makeRequestToGoogleGeoApi(self, payload):
        """
        Send payload to google geolocation api and returns json
        """
        url= GOOGLE_GEO_API_URL + GOOGLE_KEY
        r = requests.post(url, json=payload)
        print(r.json())

        return r.json()
    
    def run(self):
        """
        Init and runs ScanWifi
        """
        wifiList = self.scanWifiInformation()
        formattedList = self.formatList(wifiList)
        postjson = { "wifiAccessPoints": []}

        for i in formattedList:
            postjson['wifiAccessPoints'].append(self.convertToJson(i))
        
        self.makeRequestToGoogleGeoApi(postjson)


if __name__ == "__main__":
    Geolocation().run()