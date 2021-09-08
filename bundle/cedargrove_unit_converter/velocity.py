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
`velocity` - Speed/Velocity Converters
================================================================================
A CircuitPython module for speed/velocity conversion.

* Author(s): Cedar Grove Studios
"""

# Meters-Per-Second to Feet-Per-Second converter
def mps_to_fps(velocity_mps):
    return velocity_mps * 3.28084


# Feet-Per-Second to Meters-Per-Second converter
def fps_to_mps(velocity_fps):
    return velocity_fps / 3.28084


# Kilometers-Per_Hour to Miles-Per_Hour converter
def kmph_to_mph(velocity_kmph):
    return velocity_kmph * 0.621427


# Miles-Per_Hour to Kilometers-Per_Hour converter
def mph_to_kmph(velocity_mph):
    return velocity_mph / 0.621427


# Knots to Kilometers-Per-Hour converter
def knots_to_kmph(velocity_knots):
    return velocity_knots * 1.85184


# Kilometers-Per-Hour to Knots converter
def kmph_to_knots(velocity_kmph):
    return velocity_kmph / 1.85184


# Knots to Miles-Per-Hour converter
def knots_to_mph(velocity_knots):
    return velocity_knots * 1.150783


# Miles-Per-Hour to Knots converter
def mph_to_knots(velocity_mph):
    return velocity_mph / 1.150783


# Velocity of Light constant (meters-per-second)
def velocity_of_light():
    return 299792458


# Velocity of Sound constant (meters-per-second) in air, water, steel
def velocity_of_sound(medium="air"):
    if medium == "air":
        return 343  # 20deg_c at 1.0 atm
    if medium == "water":
        return 1481
    if medium == "steel":
        return 5120
    return None
