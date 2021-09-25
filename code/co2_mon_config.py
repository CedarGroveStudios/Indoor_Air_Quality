# air_mon_config.py

from air_mon_colors import *

ALT_LANGUAGE = "FRANCAIS"  # DEUTSCH, FRANCAIS, or PIRATE
TRANSLATE = False  # Start-up with alternate language
TEMP_UNIT = "F"  # "F" for Fahrenheit, "C" for Celsius
BRIGHTNESS = 0.50  # 0.0 to 1.0; 0.75 is typical
SENSOR_INTERVAL = 10  # Interval between measurements (2 to 1800 seconds)

CO2_ALARM = [2500, RED, "Alarm"]  # CO2 concentration; parts-per-million (PPM)
