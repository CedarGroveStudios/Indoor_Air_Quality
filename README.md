# Cedar Grove Indoor Air Quality Monitor

### _A portable indoor CO2 montor_

## Overview

The Indoor Air Quality Monitor is a portable SCD-30-based ambient CO2 measurement device implemented using CircuitPython version 6.3.0, tuned for the Adafruit PyBadge (https://www.adafruit.com/product/4200) and PyGamer (https://www.adafruit.com/product/4242) handheld gaming platforms. Features include graphical and numeric display of measured CO2, qualitative descriptor, and user-configurable alarm setting. The PyBadge/PyGamer platform provides the color display, speaker for the audible alarm (https://www.adafruit.com/product/4227), and room for a LiPo rechargeable battery (https://www.adafruit.com/product/4237). The Adafruit Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor breakout (https://www.adafruit.com/product/4867) is connected to the PyBadge/PyGamer STEMMA connector.

The Indoor Air Quality Monitor bundle folder contains all the files and helpers needed for CircuitPython version 6.x.

Editable user-specified configuration parameters are stored in the _co2_mon_config.py_ file. The configuration file specifies start-up temperature units, CO2 alarm threshold, and alternate language. Currently, only English, German, and French language translations are supported, but more are planned.

The primary Indoor Air Quality code module detects and adjusts automatically for display resolution including font size (an older version without automatic font sizing is shown in the photo). The code was successfully tested on the PyBadge, PyGamer, EdgeBadge, PyPortal, PyPortal Pynt, PyPortal Titano, FunHouse, and CLUE boards without requiring code modification.

Forced CO2 sensor calibration is initiated by pressing and holding the _START_ button on the PyBadge/PyGamer/EdgeBadge for one second. Forced calibration is initiated by touching and holding the middle portion of the PyPortal touchscreen or pressing and holding the FunHouse center button. Forced calibration is not supported on the CLUE.

Pressing and holding the PyBadge _SELECT_ button changes temperature units. Touch and hold the lower portion of the PyPortal touchscreen, press and hold the CLUE  _B_ button, or the FunHouse lower button.

The PyBadge _A_ button toggles between languages. To switch languages on the PyPortal, touch and hold the upper portion of the touchscreen. Press and hold the CLUE _A_ button or the FunHouse top button to switch languages.

Thank you to @effiksmusic and @DavidGlaude for alternate language translations (German, French). 

![Image of Module](https://github.com/CedarGroveStudios/Indoor_Air_Quality/blob/main/photos_and_graphics/co2_monitor_board_line-up_v2.png)
