# Cedar Grove Indoor Air Quality Monitor

### _A portable indoor CO2 montor_

## Overview

The Indoor Air Quality Monitor is a portable SCD-30-based ambient CO2 measurement device implemented using CircuitPython version 6.x tuned for the Adafruit PyBadge (https://www.adafruit.com/product/4200) and PyGamer (https://www.adafruit.com/product/4242) handheld gaming platforms. Features include graphical and numeric display of measured CO2, qualitative descriptor, and user-configurable alarm setting. The PyBadge/PyGamer platform provides the color display, speaker for the audible alarm (https://www.adafruit.com/product/4227), and room for a LiPo rechargeable battery (https://www.adafruit.com/product/4237). The Adafruit Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor breakout (https://www.adafruit.com/product/4867) is connected to the PyBadge/PyGamer STEMMA connector.

The Indoor Air Quality Monitor bundle folder contains all the files and helpers needed for CircuitPython version 6.x.

Editable user-specified configuration parameters are stored in the _co2_mon_config.py_ file. Besides selecting initial temperature units and display brightness, the configuration file supports language translation.

The primary Indoor Air Quality code module detects and adjusts automatically for display resolution including font size (an older version without automatic font sizing is shown in the photo). The code was successfully tested on the EdgeBadge, PyPortal, PyPortal Pynt, PyPortal Titano, FunHouse, and Clue boards without requiring modification.

Forced calibration is initiated by pressing the _START_ button on the PyBadge/PyGamer/EdgeBadge. Pressing _SELECT_ changes temperature units. The _A_ button toggles between languages. Button selections are not supported on other boards at this time.

![Image of Module](https://github.com/CedarGroveStudios/Indoor_Air_Quality/blob/main/photos_and_graphics/co2_monitor_board_line-up.png)
