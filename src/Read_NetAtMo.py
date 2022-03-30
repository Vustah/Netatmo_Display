# import netatmo

# netatmo.fetch()
import os
import lnetatmo
from pwinput import pwinput
import socket
import time
import datetime
import threading
import sys
from sevenSegment import sevenSegment

def list_all_parameters(station):
    for key_1 in station:
        data = station[key_1]
        if isinstance(data, dict):
            print(key_1)
            for key_2 in data:
                print("--->", key_2, data[key_2])
        elif isinstance(data, list):
            for element in data:
                if isinstance(element, dict):
                    print(key_1)
                    for key_2 in element:
                        print("----->", key_2, element[key_2])
        else:
            print(key_1, data)


def setup():
    username = input("Type username: ")
    password = pwinput("Type password: ")
    
    if not(isinstance(username,str) and isinstance(password,str)): return False

    credentials = {"NETATMO_CLIENT_ID": "61a3c0627d508c2896196327",
                   "NETATMO_CLIENT_SECRET": "gjqSM5c32QNdRuTZWtrYCojSOAGAyERT3JzagXK1P8",
                   "NETATMO_USERNAME": username,
                   "NETATMO_PASSWORD": password,
                   "DEVICE": "70:ee:50:3e:f3:be"}

    return credentials


def refresh_sensors(credentials):
    # Access to the sensors
    try:
        auth = lnetatmo.ClientAuth( clientId=credentials["NETATMO_CLIENT_ID"],
                                    clientSecret=credentials["NETATMO_CLIENT_SECRET"],
                                    username=credentials["NETATMO_USERNAME"],
                                    password=credentials["NETATMO_PASSWORD"],
                                    scope="read_station")

    except lnetatmo.AuthFailure as e:
        print(e, end=" ")
        print("\nWrong password or username.")
        return None
    except socket.timeout as e:
        print(e, end=" ")
        print("\nA timeout occoured.")
        return None

    try:
        dev = lnetatmo.WeatherStationData(auth)
        stations = dev.stationByName()
        return stations
    except TypeError as e:
        print(e)
        pass
        return None


def getTemperatureString(stations):
    time_now = datetime.datetime.now()
    today = datetime.date.today()
    
    temp_str = today.strftime("%d/%m/%Y") +" "+ time_now.strftime("%H:%M:%S")
    temp_str += "\t|{moduleName}: {temperature} degC\t".format(moduleName=stations["module_name"],temperature=str(stations["dashboard_data"]["Temperature"]) )
    
    for module in stations["modules"]:
        temp_str += "|{moduleName}: {temperature} degC".format(moduleName=module["module_name"],temperature=str(module["dashboard_data"]["Temperature"]))
    return temp_str

def refresh_and_print(stations):
    printstring = getTemperatureString(stations)
    print(printstring)

    
def display_temperature(display_unit,temp):
    ten_parts = int(((temp*10)%10)/10)
    ones = int(temp%10)
    tens = int((temp%100-ones)/10)

    display_unit.clear_display()
    display_unit.place_cursor(0x1)
    display_unit.write_number(tens)
    display_unit.write_number(ones)
    display_unit.decimal_control(0b00000100)
    display_unit.write_number(ten_parts)

    
def fetch_and_write_temp(credentials):
    indoor_display = sevenSegment(0x71)
    while(1):
        stations = refresh_sensors(credentials)
        # list_all_parameters(stations)
        if stations == None:
            break
        if stations["module_name"] == "Stue":
            print("sending Stue_temp {temperature} to display".format(temperature=stations["dashboard_data"]["Temperature"]))
            display_temperature(indoor_display,stations["dashboard_data"]["Temperature"])
        time.sleep(5)
#        refresh_and_print(stations)
        
        

if __name__ == "__main__":

    credentials = setup()
    fetch_and_write_temp(credentials)
    
#    temp_thread = threading.Thread(target=fetch_and_write_temp,args=([credentials]))
  #  temp_thread.start()
