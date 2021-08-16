# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# co2_monitor.py
# 2021-08-15 v1.2

import time
import board
import busio
import os
import displayio
import neopixel
from analogio import AnalogIn
from digitalio import DigitalInOut
from simpleio import tone
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import adafruit_scd30
from index_to_rgb.stoplight_spectrum import index_to_rgb
from thermal_cam_converters import celsius_to_fahrenheit, fahrenheit_to_celsius
from co2_mon_config import (
    ALARM_CO2,
    CO2_GOOD,
    CO2_POOR,
    CO2_WARNING,
    CO2_DANGER,
    CO2_MAXIMUM,
    SENSOR_INTERVAL,
)

board_type = os.uname().machine
if "Pybadge" or "Pygamer" in board_type:
    battery_mon = AnalogIn(board.A6)
    has_battery_mon = True
else:
    has_battery_mon = False

# Instantiate SCD-30 with reliable I2C clock frequency (50KHz)
try:
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)
except:
    print("---------------------")
    print("--- SCD30 SENSOR  ---")
    print("--- NOT CONNECTED ---")
    print("---------------------")
    while True:
        pass

# Instantiate display, fonts, speaker, and neopixels
display = board.DISPLAY
display.brightness = 0.75
WIDTH = display.width
HEIGHT = display.height
# Load the text font from the fonts folder
if WIDTH > 160:
    font_0 = bitmap_font.load_font("/fonts/OpenSans-12.bdf")
    font_1 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")
else:
    font_0 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
    font_1 = bitmap_font.load_font("/fonts/OpenSans-16.bdf")
# Turn on speaker output
if hasattr(board, "SPEAKER_ENABLE"):
    speaker_enable = DigitalInOut(board.SPEAKER_ENABLE)
    speaker_enable.switch_to_output(value=True)
# Set NeoPixel brightness and clear all pixels
if hasattr(board, "NEOPIXEL"):
    has_neopixel = True
    pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, pixel_order=neopixel.GRB)
    pixels.brightness = 0.05
    pixels.fill(0x000000)
else:
    has_neopixel = False

# Define a few colors
BLACK = 0x000000
RED = 0xFF0000
RED_DK = 0xA00000
YELLOW = 0xFFFF00
YELLOW_DK = 0x202000
CYAN = 0x00FFFF
BLUE = 0x0000FF
BLUE_DK = 0x000080
WHITE = 0xFFFFFF
ORANGE = 0xFFA000
GREEN = 0x00A000
GRAY = 0x508080


# ### Helpers ###
def play_tone(freq=440, duration=0.01):
    """ Play tones through the integral speaker. """
    tone(board.A0, freq, duration)
    return


def flash_status(text="", duration=0.05):
    """ Flash a status message once. """
    status_label.color = WHITE
    status_label.text = text
    time.sleep(duration)
    status_label.color = BLACK
    time.sleep(duration)
    status_label.text = ""
    return


def update_image_frame(blocking=False):
    """Acquire SCD-30 data and update the display. When blocking = True, the
    function will wait until the sensor is ready, up to 3 seconds. When
    blocking = False, the function will immediately return if the sensor data
    is not available."""
    t0 = time.monotonic()
    while blocking and (not scd.data_available) and (t0 - time.monotonic() < 3):
        watchdog.fill = RED
        flash_status("WARMUP", 0.5)

    if scd.data_available:
        watchdog.fill = YELLOW  # Data acquisition indicator: active
        sensor_co2 = round(scd.CO2)  # Retrieve quality data and round value

        sensor_co2_normalized = (
            sensor_co2 / CO2_MAXIMUM
        )  # Normalized to 0.0 to 1.0 (for plotting)
        sensor_rh = round(
            scd.relative_humidity
        )  # Retrieve humidity data and round value
        sensor_temp_c = round(
            scd.temperature
        )  # Retrieve temperature data and round value
        sensor_temp_f = round(
            celsius_to_fahrenheit(sensor_temp_c)
        )  # Convert to Fahrenheit

        if sensor_co2 <= CO2_MAXIMUM:
            # Plot quality pointer on scale; adjust fill color for sensor value
            pointer.fill = index_to_rgb(sensor_co2_normalized)
            pointer.y = HEIGHT - int(sensor_co2_normalized * HEIGHT)
            pointer_shadow.y = pointer.y
        else:
            # If quality is out-of-range, pin the pointer and show a warning
            pointer.fill = RED
            pointer.y = 0
            sensor_co2 = CO2_MAXIMUM
            flash_status("OVERLOAD", 0.75)

        # Update on-screen values
        co2_value.text = str(sensor_co2)
        humidity_value.text = str(sensor_rh)
        temperature_value.text = str(sensor_temp_f)
        alarm_value.text = str(ALARM_CO2)

        # Update quality evaluation text
        if sensor_co2 > CO2_DANGER:
            quality_label.color = RED
            quality_label.text = "DANGER"
        elif scd.CO2 > CO2_WARNING:
            quality_label.color = ORANGE
            quality_label.text = "WARNING"
        elif scd.CO2 > CO2_POOR:
            quality_label.color = YELLOW
            quality_label.text = "POOR"
        else:
            quality_label.color = GREEN
            quality_label.text = "GOOD"

        # Draw the trend chart bars
        for i in range(0, len(trend_chart)):
            trend_group[len(trend_chart) - i - 1].y = (
                HEIGHT - int(trend_chart[i] * HEIGHT) + 1
            )
            trend_group[len(trend_chart) - i - 1].fill = GRAY
        trend_chart.pop(0)  # remove oldest point from trend
        trend_chart.append(sensor_co2_normalized)  # add latest point

    watchdog.fill = YELLOW_DK  # Data acquisition indicator: completed
    return


play_tone(880, 0.1)  # A5

# ### Define the display groups ###
image_group = displayio.Group()
trend_group = displayio.Group()
reference_group = displayio.Group()

# Define trend chart group
trend_chart = []
point_width = int((WIDTH - 28) / 40)  # Save memory on large displays
for i in range(0, WIDTH - 28, point_width):
    point = Rect(
        x=(WIDTH - 28) - i,
        y=(HEIGHT - 6),
        width=point_width,
        height=HEIGHT,
        fill=None,
        outline=None,
        stroke=0,
    )
    trend_chart.insert(0, HEIGHT)
    trend_group.append(point)
image_group.append(trend_group)

# Define sensor and quality scale reference group
cell_height = int(HEIGHT / 64)  # Save memory on large displays
for i in range(0, HEIGHT + cell_height, cell_height):
    cell = Rect(
        x=WIDTH - 20,
        y=(HEIGHT + 1) - i,
        width=20,
        height=cell_height,
        fill=index_to_rgb(i / HEIGHT),
        outline=None,
        stroke=0,
    )
    reference_group.append(cell)

good_pointer = Rect(
    x=WIDTH - 22,
    y=0,
    width=10,
    height=int(((CO2_POOR - CO2_GOOD) / CO2_MAXIMUM) * HEIGHT) + 3,
    fill=GREEN,
    outline=BLACK,
    stroke=1,
)
good_pointer.y = HEIGHT - int((CO2_POOR / CO2_MAXIMUM) * HEIGHT)
reference_group.append(good_pointer)

poor_pointer = Rect(
    x=WIDTH - 22,
    y=0,
    width=10,
    height=int(((CO2_WARNING - CO2_POOR) / CO2_MAXIMUM) * HEIGHT) + 3,
    fill=YELLOW,
    outline=BLACK,
    stroke=1,
)
poor_pointer.y = HEIGHT - int((CO2_WARNING / CO2_MAXIMUM) * HEIGHT)
reference_group.append(poor_pointer)

warning_pointer = Rect(
    x=WIDTH - 22,
    y=0,
    width=10,
    height=int(((CO2_DANGER - CO2_WARNING) / CO2_MAXIMUM) * HEIGHT) + 3,
    fill=ORANGE,
    outline=BLACK,
    stroke=1,
)
warning_pointer.y = HEIGHT - int((CO2_DANGER / CO2_MAXIMUM) * HEIGHT)
reference_group.append(warning_pointer)

danger_pointer = Rect(
    x=WIDTH - 22,
    y=0,
    width=10,
    height=int(((CO2_MAXIMUM - CO2_DANGER) / CO2_MAXIMUM) * HEIGHT) + 3,
    fill=RED,
    outline=BLACK,
    stroke=1,
)
danger_pointer.y = HEIGHT - int((CO2_MAXIMUM / CO2_MAXIMUM) * HEIGHT)
reference_group.append(danger_pointer)

alarm_pointer_shadow = Rect(
    x=WIDTH - 25, y=0, width=26, height=4, fill=RED, outline=BLACK, stroke=1
)
alarm_pointer_shadow.y = HEIGHT - int((ALARM_CO2 / CO2_MAXIMUM) * HEIGHT)
reference_group.append(alarm_pointer_shadow)

alarm_pointer = Rect(
    x=WIDTH - 25, y=0, width=26, height=3, fill=RED, outline=BLACK, stroke=1
)
alarm_pointer.y = HEIGHT - int((ALARM_CO2 / CO2_MAXIMUM) * HEIGHT)
reference_group.append(alarm_pointer)

image_group.append(reference_group)

# Define quality pointer and watchdog then add to image group
pointer_shadow = Rect(
    x=WIDTH - 25, y=HEIGHT + 2, width=26, height=6, fill=None, outline=BLACK, stroke=1
)
image_group.append(pointer_shadow)

pointer = Rect(
    x=WIDTH - 25, y=HEIGHT + 2, width=26, height=5, fill=None, outline=BLACK, stroke=1
)
image_group.append(pointer)

watchdog = Rect(x=1, y=1, width=10, height=10, fill=None, outline=None, stroke=0)
image_group.append(watchdog)

# Define titles, labels, and values for the image group
title_label = Label(font_0, text="Indoor Air Quality", color=CYAN)
title_label.anchor_point = (0.5, 0)
title_label.anchored_position = ((WIDTH // 2) - 10, 0)
image_group.append(title_label)

quality_label = Label(font_1, text=" ", color=None)
quality_label.anchor_point = (0.5, 0.5)
quality_label.anchored_position = ((WIDTH // 2) - 10, HEIGHT // 4)
image_group.append(quality_label)

status_label = Label(font_0, text=" ", color=None)
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = ((WIDTH // 2) - 10, (HEIGHT // 2) + 27)
image_group.append(status_label)

alarm_label = Label(font_0, text="alarm", color=RED)
alarm_label.anchor_point = (0, 0)
alarm_label.anchored_position = (5, HEIGHT - 14)
image_group.append(alarm_label)

alarm_value = Label(font_0, text=str(ALARM_CO2), color=RED)
alarm_value.anchor_point = (0, 0)
alarm_value.anchored_position = (5, HEIGHT - 28)
image_group.append(alarm_value)

temperature_label = Label(font_0, text="F", color=CYAN)
temperature_label.anchor_point = (0.5, 0)
temperature_label.anchored_position = ((WIDTH - 20) // 2, HEIGHT - 14)
image_group.append(temperature_label)

temperature_value = Label(font_0, text=" ", color=CYAN)
temperature_value.anchor_point = (0.5, 0)
temperature_value.anchored_position = ((WIDTH - 20) // 2, HEIGHT - 28)
image_group.append(temperature_value)

humidity_label = Label(font_0, text="RH", color=CYAN)
humidity_label.anchor_point = (1, 0)
humidity_label.anchored_position = (WIDTH - 40, HEIGHT - 14)
image_group.append(humidity_label)

humidity_value = Label(font_0, text=" ", color=CYAN)
humidity_value.anchor_point = (1, 0)
humidity_value.anchored_position = (WIDTH - 40, HEIGHT - 28)
image_group.append(humidity_value)

co2_label = Label(font_0, text="PPM CO2", color=BLUE)
co2_label.anchor_point = (0.5, 0)
co2_label.anchored_position = ((WIDTH // 2) - 10, 4 + (HEIGHT // 2))
image_group.append(co2_label)

co2_value = Label(font_1, text=" ", color=WHITE)
co2_value.anchor_point = (0.5, 1.0)
co2_value.anchored_position = ((WIDTH // 2) - 10, HEIGHT // 2)
image_group.append(co2_value)

# ###--- PRIMARY PROCESS SETUP ---###
# Activate display and play welcome tones
display.show(image_group)
scd.reset()  # Reset sensor
update_image_frame(blocking=True)  # Wait for then display sensor data
scd.measurement_interval = SENSOR_INTERVAL  # Set the sensor acquisition interval

play_tone(440, 0.1)  # A4
play_tone(880, 0.1)  # A5

# ###--- PRIMARY PROCESS LOOP ---###
while True:
    update_image_frame()  # If available, acquire sensor data and update display

    # If alarm threshold is reached, flash NeoPixels, ALARM status, and play alarm tone
    if co2_value.text != " " and float(co2_value.text) >= ALARM_CO2:
        flash_status("ALARM", 0.75)
        if has_neopixel:
            pixels.fill(RED)
        play_tone(880, 0.015)  # A5
        if has_neopixel:
            pixels.fill(BLACK)

    if has_battery_mon:
        """The 3.2-volt threshold is an approximation. Each board's battery
        monitoring circuitry can vary +/-10% due to internal voltage divider
        resistor tolerance."""
        battery_volts = round(battery_mon.value * 6.6 / 0xFFF0, 2)
        if battery_volts < 3.2:
            play_tone(880, 0.030)  # A5
            flash_status("LOW BATTERY", 1)
            flash_status(str(battery_volts) + "V", 1)
