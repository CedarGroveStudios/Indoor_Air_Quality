# The MIT License (MIT)

# Copyright (c) 2020, 2021 Cedar Grove Studios

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`temperature` - Temperature Converters
================================================================================
A CircuitPython module for temperature conversion.

* Author(s): Cedar Grove Studios
"""

# Celsius to Fahrenheit converter
def celsius_to_fahrenheit(deg_c):
    return ((9 / 5) * deg_c) + 32


# Fahrenheit to Celsius converter
def fahrenheit_to_celsius(deg_f):
    return (deg_f - 32) * (5 / 9)


# Celsius to Kelvin converter
def celsius_to_kelvin(deg_c):
    return deg_c + 273.15


# Kelvin to Celsius converter
def kelvin_to_celsius(kelvins):
    return kelvins - 273.15


# Dew Point converter (degrees Celsius)
def dew_point(deg_c, humidity, verbose=False):
    message_list = (
        (-9999, 10, "Safe", ": A bit dry for some."),
        (10, 12, "Safe", ": Very comfortable."),
        (13, 16, "Safe", ": Comfortable."),
        (16, 18, "Safe", ": Okay for most."),
        (18, 21, "Caution", ": Somewhat uncomfortable for most people."),
        (21, 24, "Caution", ": Very humid, quite uncomfortable."),
        (24, 26, "Extreme Caution", ": Extremely uncomfortable, fairly oppresive."),
        (
            26,
            9999,
            "DANGER",
            ": Severely high, potentially deadly for asthma sufferers.",
        ),
    )

    dew_point_c = round(
        (
            pow(humidity / 100.0, 0.125) * (112.0 + (0.9 * deg_c))
            + (0.1 * deg_c)
            - 112.0
        ),
        2,
    )

    # Constrain dew_point to range of 0 to 40 degrees Celsius
    dew_point_c = min(max(dew_point_c, 0), 40)

    if verbose:
        # Select range message from list
        for i in range(0, len(message_list)):
            if message_list[i][0] <= dew_point_c < message_list[i][1]:
                return dew_point_c, message_list[i][2] + message_list[i][3]
    return dew_point_c


# Heat/Comfort index (degrees Celsius)
# (source: https://en.wikipedia.org/wiki/Heat_index)
def heat_index(deg_c, humidity, verbose=False):
    message_list = (
        (-99, 26, "Safe", ": Heat index is not a factor.", ""),
        (
            26,
            32,
            "Caution",
            ": Fatigue is possible with prolonged exposure and activity. ",
            "Continuing activity could result in heat cramps.",
        ),
        (
            32,
            41,
            "Extreme Caution",
            ": Heat cramps and heat exhaustion are possible. ",
            "Continuing activity could result in heat stroke.",
        ),
        (
            41,
            54,
            "DANGER",
            ": Heat cramps and heat exhaustion are likely. ",
            "Heat stroke is probable with continued activity.",
        ),
        (54, 99, "EXTREME DANGER", ": Heat stroke is imminent. ", ""),
    )

    t = ((9 / 5) * deg_c) + 32  # Dry-bulb temperature in degrees Fahrenheit
    r = humidity  # Percentage value between 0 and 100

    # Fahrenheit coefficients
    c = (
        0,
        -42.379,
        2.04901523,
        10.14333127,
        -0.22475541,
        -0.00683783,
        -0.05481717,
        0.00122874,
        0.00085282,
        -0.00000199,
    )

    # Formula (Fahrenheit method, +/-1.3F: Rothfusz NWS-SR90-23, 1990)
    # https://www.weather.gov/media/ffc/ta_htindx.PDF
    h_index_f = round(
        c[1]
        + (c[2] * t)
        + (c[3] * r)
        + (c[4] * t * r)
        + (c[5] * t ** 2)
        + (c[6] * r ** 2)
        + (c[7] * t ** 2 * r)
        + (c[8] * t * r ** 2)
        + (c[9] * t ** 2 * r ** 2),
        1,
    )
    # Convert to degrees Celsius
    h_index_c = round((h_index_f - 32) * (5 / 9), 1)

    if verbose:
        # Select range message from list
        for i in range(0, len(message_list)):
            if message_list[i][0] <= h_index_c < message_list[i][1]:
                return h_index_c, (
                    message_list[i][2] + message_list[i][3] + message_list[i][4]
                )
    return h_index_c


def wind_chill(deg_c, wind_vel_kmph, verbose=False):
    # (source: https://en.wikipedia.org/wiki/Wind_chill)
    pass
    return


def apparent_temperature(deg_c, humidity, wind_vel_kmph, verbose=False):
    # Australian apparent temperature (AT); thermal sensation
    # (source: https://en.wikipedia.org/wiki/Wind_chill)
    pass
    return
