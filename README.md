# Cedar Grove Indoor Air Quality Monitor

### _A portable indoor CO2 montor_

## Overview

The Indoor Air Quality Monitor is a portable SCD-30-based ambient CO2 measurement device implemented using CircuitPython version 6.x on an Adafruit PyBadge (https://www.adafruit.com/product/4200) and PyGamer (https://www.adafruit.com/product/4242) handheld gaming platforms. Features include graphical and numeric display of measured CO2, qualitative descriptor, and user-configurable alarm setting. The PyBadge/PyGamer platform provides the color display, speaker for the audible alarm (https://www.adafruit.com/product/4227), and room for a LiPo rechargeable battery (https://www.adafruit.com/product/4237). The Adafruit Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor breakout (https://www.adafruit.com/product/4867) is connected to the PyBadge/PyGamer STEMMA connector.

The Indoor Air Quality Monitor utilizes a number of PyBadge-stored files and conversion helpers in order to operate. The bundle folder contains all the files and helpers needed for CircuitPython version 6.x.

Editable user-specified configuration parameters are stored in the _co2_mon_config.py_ file.

Note: The primary Indoor Air Quality code module detects and adjusts automatically for display resolution -- although at this time, font sizes are fixed and look a little weird on the larger displays. The code was successfully tested on the PyPortal, PyPortal Pynt, and Clue boards without modification. Also, this version will only work on boards with NeoPixel indicators. Full board independence is a future possibility.

![Image of Module](https://github.com/CedarGroveStudios/Indoor_Air_Quality/blob/main/photos_and_graphics/IMG_0719.jpeg)
