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
`chronos` - Time Converters
================================================================================
A CircuitPython module for time converters.

* Author(s): Cedar Grove Studios
"""

import time


def leap_year(year):
    """Detects if the input is a valid leap year. """
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True  # leap year
            else:
                return False  # not leap year
        else:
            return True  # leap year
    return False  # not leap year


def detect_dst(datetime):
    """Detects North American Daylight Saving Time from Standard Time.
    Input to this helper is expressed as a structured time object in
    Standard Time (xST). The helper cannot detect DST for a DST
    structured time object.
        Returns:    True if datetime is North American DST
                    False if datetime is xST"""

    # Fix weekday and yearday structured time errors
    datetime = time.localtime(time.mktime(datetime))

    # Convert Python time structure Monday-origin to Sunday-origin.
    weekday = (datetime.tm_wday + 1) % 7

    # Get the date of the previous Sunday or today's date if Sunday.
    prev_sunday_date = datetime.tm_mday - weekday

    # March: Second Sunday occurs on the 8th through 14th of the month at
    #   02:00 Standard Time (xST).
    if datetime.tm_mon == 3:
        if prev_sunday_date <= 7:  # First Sunday of month or before
            return False  # xST
        if prev_sunday_date <= 14:  # Second Sunday of month
            # determine current DST threshold
            # year, March, previous Sunday date, 02 hours xST, 00 min, 00 sec
            dst_thresh = time.mktime(
                time.struct_time(
                    (datetime.tm_year, 3, prev_sunday_date, 2, 0, 0, 0, -1, -1)
                )
            )
            if time.mktime(datetime) < dst_thresh:
                return False  # xST
        return True  # DST

    # November: First Sunday occurs on the 1st through 7th of the month at
    #    01:00 Standard Time (xST) = 02:00 Daylight Saving Time (xDT)
    if datetime.tm_mon == 11:
        if prev_sunday_date < 1:  # Before first Sunday of month
            return True  # DST
        if prev_sunday_date <= 7:  # First Sunday of month
            # determine current xST threshold
            # year, November, previous Sunday date, 01 hours xDT, 00 min, 00 sec
            xst_thresh = time.mktime(
                time.struct_time(
                    (datetime.tm_year, 11, prev_sunday_date, 1, 0, 0, 0, -1, -1)
                )
            )
            if time.mktime(datetime) < xst_thresh:
                return True  # DST
        return False  # xST

    # Check for Standard Time
    if datetime.tm_mon < 3 or datetime.tm_mon > 11:  # Dec - Feb: xST
        return False  # xST
    return True  # DST
    # if datetime.tm_mon > 3 and datetime.tm_mon < 11:  # Apr - Oct: DST
    #    return True   # DST


def adjust_dst(datetime):
    """Converts Standard Time to North American Daylight Saving Time.
    Input to this helper is a structured time object in Standard Time (xST).
    The helper returns a structured time object adjusted to a DST value if
    appropriate and a flag indicating DST. Input to this helper is expressed
    as a structured time object in Standard Time (xST). The helper cannot
    detect DST for a DST structured time object."""

    is_dst = detect_dst(datetime)  # Determine if datetime is DST

    if is_dst:  # If DST, add an hour
        dst_date_time = time.mktime(datetime) + 3600
        return time.localtime(dst_date_time), True
    return datetime, False
