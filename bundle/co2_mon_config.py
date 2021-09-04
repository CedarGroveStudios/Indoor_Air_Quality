# co2_mon_config.py
# ### Alarm and range default values in PPM ###

# English Translation
SCREEN_TITLE = "Indoor Air Quality"
TEMP_UNIT = "F"  # "F" for Fahrenheit, "C" for Celsius
WARMUP_STATUS = "WARMUP"
OVERLOAD_STATUS = "OVERLOAD"

ALARM_CO2 = [2500, "Alarm"]

CO2_GOOD = [0, "GOOD"]
CO2_POOR = [1000, "POOR"]
CO2_WARNING = [2000, "WARNING"]
CO2_DANGER = [5000, "DANGER"]

CO2_MAXIMUM = 6000  # Maximum scale display value

SENSOR_INTERVAL = 30  # Interval between measurements (2 to 1800 seconds)

"""# German Translation
SCREEN_TITLE = "Raumluftqualität"
TEMP_UNIT = "C"  # "F" for Fahrenheit, "C" for Celsius
WARMUP_STATUS = "WARMUP"
OVERLOAD_STATUS = "OVERLOAD"

ALARM_CO2 = [2500, "Alarm"]

CO2_GOOD = [0, "GUT"]
CO2_POOR = [1000, "SCHLECHT"]
CO2_WARNING = [2000, "WARNUNG"]
CO2_DANGER = [5000, "GEFAHR"]

CO2_MAXIMUM = 6000  # Maximum scale display value

SENSOR_INTERVAL = 30  # Interval between measurements (2 to 1800 seconds)"""
