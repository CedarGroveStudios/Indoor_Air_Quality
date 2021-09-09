# SPDX-FileCopyrightText: 2021 Cedar Grove Studios
# SPDX-License-Identifier: MIT

# aqi_air_quality.py
# 2021-09-07 version 1.0

# EPA Air Quality Index (AQI) as derived from PM2.5 particulate concentration

RED = 0xFF0000
YELLOW = 0xFFFF00
BLUE = 0x0000FF
ORANGE = 0xFFA500
GREEN = 0x00FF00
PURPLE = 0x800080
MAROON = 0x800000


def map_range(x, in_min, in_max, out_min, out_max):
    """
    Maps and constrains an input value from one range of values to another.
    (from adafruit_simpleio)
    :return: Returns value mapped to new range
    :rtype: float
    """
    in_range = in_max - in_min
    in_delta = x - in_min
    if in_range != 0:
        mapped = in_delta / in_range
    elif in_delta != 0:
        mapped = in_delta
    else:
        mapped = 0.5
    mapped *= out_max - out_min
    mapped += out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)


def concentration_to_aqi(pm25_value):
    """Returns a data valid flag, calculated air quality index (AQI), color,
    and category.
    NOTE: The AQI returned by this function should ideally be measured
    using the 24-hour concentration average. Calculating a AQI without
    averaging will result in higher AQI values than expected.
    :param float pm_sensor_reading: Particulate matter sensor value,
    2.5 particle size.
    """
    # Check sensor reading using EPA breakpoints
    if pm25_value > 500:
        return True, 500, MAROON, "OVERRANGE"
    elif pm25_value > 350:
        aqi_value = int(map_range(pm25_value, 350, 500, 400, 500))
        return True, aqi_value, MAROON, "HAZARDOUS"
    elif pm25_value > 250:
        aqi_value = int(map_range(pm25_value, 250, 350, 300, 400))
        return True, aqi_value, MAROON, "HAZARDOUS"
    elif pm25_value > 150:
        aqi_value = int(map_range(pm25_value, 150, 250, 200, 300))
        return True, aqi_value, PURPLE, "V UNHEALTHY"
    elif pm25_value > 55:
        aqi_value = int(map_range(pm25_value, 55, 150, 150, 200))
        return True, aqi_value, RED, "UNHEALTHY"
    elif pm25_value > 35:
        aqi_value = int(map_range(pm25_value, 35, 55, 100, 150))
        return True, aqi_value, ORANGE, "SENSITIVE"
    elif pm25_value > 12:
        aqi_value = int(map_range(pm25_value, 12, 35, 50, 100))
        return True, aqi_value, YELLOW, "MODERATE"
    elif pm25_value > 0:
        aqi_value = int(map_range(pm25_value, 0, 12, 0, 50))
        return True, aqi_value, GREEN, "GOOD"
    return False, -1, BLUE, "INVALID"
