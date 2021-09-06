# air_mon_config.py
# ### Alarm and range default values in PPM ###

from air_mon_colors import *

# English Translation
SCREEN_TITLE = "Air Quality"
TEMP_UNIT = "F"  # "F" for Fahrenheit, "C" for Celsius
WARMUP_STATUS = "WARMUP"
OVERLOAD_STATUS = "OVERLOAD"

CO2_ALARM = [2500, RED, "Alarm"]
CO2_GOOD = [0, GREEN, "GOOD"]
CO2_POOR = [1000, YELLOW, "POOR"]
CO2_WARNING = [2000, ORANGE, "WARNING"]
CO2_DANGER = [5000, RED, "DANGER"]
CO2_MAXIMUM = 6000  # Maximum CO2 scale display value

AQI_ALARM = [150, RED, "Alarm"]
AQI_GOOD = [0, GREEN, "GOOD"]
AQI_MODERATE = [50, YELLOW, "MODERATE"]
AQI_SENS_UNHEALTHY = [100, ORANGE, "SENSITIVE"]
AQI_UNHEALTHY = [150, RED, "UNHEALTHY"]
AQI_VERY_UNHEALTHY = [200, PURPLE, "V UNHEALTH"]
AQI_HAZARDOUS = [300, MAROON, "HAZARDOUS"]
AQI_MAXIMUM = 500  # Maximum AQI scale display value

SENSOR_INTERVAL = 10  # Interval between measurements (2 to 1800 seconds)

"""# German Translation
SCREEN_TITLE    = "Raumluftqualität"
TEMP_UNIT       = "C"  # "F" for Fahrenheit, "C" for Celsius
WARMUP_STATUS   = "WARMUP"
OVERLOAD_STATUS = "OVERLOAD"

CO2_ALARM   = [2500, RED,    "Alarm"]
CO2_GOOD    = [0,    GREEN,  "GUT"]
CO2_POOR    = [1000, YELLOW, "SCHLECHT"]
CO2_WARNING = [2000, ORANGE, "WARNUNG"]
CO2_DANGER  = [5000, RED,    "GEFAHR"]
CO2_MAXIMUM = 6000  # Maximum CO2 scale display value

AQI_ALARM          = [150, RED,    "Alarm"]
AQI_GOOD           = [0,   GREEN,  "GUT"]
AQI_MODERATE       = [51,  YELLOW, "---"]
AQI_SENS_UNHEALTHY = [101, ORANGE, "---"]
AQI_UNHEALTHY      = [151, RED,    "---"]
AQI_VERY_UNHEALTHY = [201, PURPLE, "---"]
AQI_HAZARDOUS      = [301, MAROON, "---"]
AQI_MAXIMUM        = 500  # Maximum AQI scale display value

SENSOR_INTERVAL = 10  # Interval between measurements (2 to 1800 seconds)"""
