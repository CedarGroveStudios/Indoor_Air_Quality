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
`electronics` - Electronics Converters and Calculators
================================================================================
A CircuitPython module for electronics converters and calculators.

* Author(s): Cedar Grove Studios
"""

# Ohms' Law calculator/converter
def ohms_law(ohms=None, milliamperes=None, volts=None):
    """When only two numeric values are supplied (or two numeric values and
    a third =None value), the two numeric values are used to calculate and
    return the missing (or =None) value."""

    if (ohms, milliamperes, volts).count(None) > 1:
        raise ValueError("At least two values must be provided.")

    # Calculate resistance in Ohms
    if ohms == None:
        return volts / (milliamperes / 1000.0)

    # Calculate current in milliamperes (mA)
    if milliamperes == None:
        return (volts / ohms) * 1000.0

    # Calculate voltage in volts
    if volts == None:
        return ohms * (milliamperes / 1000.0)

    raise ValueError("Too many values. Only two are needed.")
