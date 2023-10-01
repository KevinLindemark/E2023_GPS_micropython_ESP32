# GPS program
from machine import UART
from gps_bare_minimum import GPS_Minimum

import _thread
import time

#########################################################################
# CONFIGURATION

gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
gps_echo = True                            # Echo NMEA frames: True or False
gps_all_NMEA = False                       # Enable all NMEA frames: True or False

threaded = True                            # Use threaded (True) or loop (False)

#########################################################################
# OBJECTS

uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation

#########################################################################    
# PROGRAM

# Dictionary til at opbevare GPS data så det nemt kan tilgås
# Ved at anvende denne undgår man et delay i programmet
# når der ventes på at GPS data kommer over UART
gps_data = {
    "UTC YYYY-MM-DD": 0,
    "UTC HH:MM:SS": 0,
    "lontitude" : -999,
    "latitude": -999,
    "validity": "V",
    "speed": 0,
    "course:": 0.0,
    "frames": 0,
    "adafruit format": 0
    }

print("GPS test program\n")

def gps_tread():
    while True:
        if gps.receive_nmea_data(gps_echo):
            #print("UTC YYYY-MM-DD: %04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day()))
            gps_data["UTC YYYY-MM-DD"] = "%04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day())
            #print("UTC HH:MM:SS  : %02d:%02d:%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds()))
            gps_data["UTC HH:MM:SS"] = "%04d-%02d-%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds())
            #print("Latitude      : %.8f" % gps.get_latitude())
            gps_data["latitude"] = "%.8f" % gps.get_latitude()
            #print("Longitude     : %.8f" % gps.get_longitude())
            gps_data["longtidude"] = "%.8f" % gps.get_longitude()
            #print("Validity      : %s" % gps.get_validity())
            gps_data["validity"] = "%s" % gps.get_validity()
            #print("Speed         : %.1f m/s" % gps.get_speed())
            gps_data["speed"] = "%.1f m/s" % gps.get_speed()
            #print("Course        : %.1f°" % gps.get_course())
            gps_data["course"] = "%.1f°" % gps.get_course()
          
            # adafruit format: speed,lat,lon,alt
            # example: 0.057412,55.69593,12.54784,22.4
            # altitude is fixed to 0.0 as it is not included in the $GPRMC frame
            adafruit_format = str(gps.get_speed())+","+str(gps.get_latitude())+","+str(gps.get_longitude())+","+"0.0"
            print(adafruit_format)
            gps_data["adafruit format"] = adafruit_format
            print(gps_data)
    
        time.sleep(1)
 
_thread.start_new_thread(gps_tread, ())