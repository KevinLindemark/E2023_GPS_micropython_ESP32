import umqtt_robust2 as mqtt
from machine import Pin, reset, UART
from time import sleep
# GPS programs
from gps_bare_minimum import GPS_Minimum

#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation
missed_gps_frames = 0 # variable til at tælle antal gange der ikke kommer et NMEA frame i while loop
#########################################################################   
def get_adafruit_gps():
    if gps.receive_nmea_data():
        # hvis der er kommet end bruggbar værdi på alle der skal anvendes
        if gps.get_speed() != 0 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0:
            # returnerer data med adafruit gps format
            return str(gps.get_speed())+","+str(gps.get_latitude())+","+str(gps.get_longitude())+","+"0.0"
        else:
            return False
# Her kan i placere globale varibaler, og instanser af klasser
led1 = Pin(26, Pin.OUT)

while True:
    try:
        led1.value(not led1.value())
        # Hvis funktionen returnere en string er den True ellers returnere den False
        if get_adafruit_gps():
            print(f'\ngps_data er: {get_adafruit_gps()}')
            mqtt.web_print(get_adafruit_gps(), 'KEA_ITTEK/feeds/mapfeed/csv')
            
        #For at sende beskeder til andre feeds kan det gøres sådan:
        # mqtt.web_print("Besked til anden feed", DIT_ADAFRUIT_USERNAME/feeds/DIT_ANDET_FEED_NAVN/ )
        #Indsæt eget username og feednavn til så det svarer til dit eget username og feed du har oprettet

        #For at vise lokationsdata på adafruit dashboard skal det sendes til feed med /csv til sidst
        #For at sende til GPS lokationsdata til et feed kaldet mapfeed kan det gøres således:
        #mqtt.web_print(gps_data, 'DIT_ADAFRUIT_USERNAME/feeds/mapfeed/csv')        
        sleep(4) # vent mere end 3 sekunder mellem hver besked der sendes til adafruit
        
        #mqtt.web_print("test1") # Hvis der ikke angives et 2. argument vil default feed være det fra credentials filen      
        #sleep(4)  # vent mere end 3 sekunder mellem hver besked der sendes til adafruit
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()