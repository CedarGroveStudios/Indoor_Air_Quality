# SPDX-FileCopyrightText: 2021 Cedar Grove Studios
# SPDX-License-Identifier: MIT

# co2_air_quality.py
# 2021-09-07 version 1.0

# Indoor Air Quality as derived from CO2 concentration

RED = 0xFF0000
YELLOW = 0xFFFF00
BLUE = 0x0000FF
ORANGE = 0xFFA500
GREEN = 0x00FF00

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


# returns ppm valid flag, ppm value, quality color, quality description
def co2_ppm_to_quality(ppm_value):
    """Returns a data valid flag, calculated ppm value, color,
    and category.
    :param float ppm_value: CO2 concentration, parts-per-million (PPM).
    """
    # Check sensor reading using ??? breakpoints
    if ppm_value > 6000:
        return True, 6000, RED, "OVERRANGE"
    elif ppm_value > 5000:
        return True, ppm_value, RED, "DANGER"
    elif ppm_value > 2000:
        return True, ppm_value, ORANGE, "WARNING"
    elif ppm_value > 1000:
        return True, ppm_value, YELLOW, "POOR"
    elif ppm_value > 100:
        return True, ppm_value, GREEN, "GOOD"
    return False, ppm_value, BLUE, "INVALID"
