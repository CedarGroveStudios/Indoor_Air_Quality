# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# co2_monitor_code.py
# 2021-09-13 v1.6.4

import time
import board
import busio
import os
import displayio
import neopixel
import random
from analogio import AnalogIn
from digitalio import DigitalInOut
from simpleio import tone
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import adafruit_scd30
from cedargrove_unit_converter.index_to_rgb.stoplight_spectrum import index_to_rgb
from cedargrove_unit_converter.temperature import celsius_to_fahrenheit
from cedargrove_unit_converter.air_quality.co2_air_quality import co2_ppm_to_quality
from cedargrove_unit_converter.air_quality.interpreter.english_to_deutsch import (
    interpret,
)
from co2_mon_config import *

SCREEN_TITLE = "Indoor Air Quality"
if LANGUAGE == "ENGLISH":
    TRANSLATE = False
else:
    TRANSLATE = True

board_type = os.uname().machine
if ("Pybadge" or "Pygamer") in board_type:
    from gamepadshift import GamePadShift

    # Define and instantiate front panel buttons
    BUTTON_LEFT = 0b10000000
    BUTTON_UP = 0b01000000
    BUTTON_DOWN = 0b00100000
    BUTTON_RIGHT = 0b00010000
    BUTTON_SELECT = 0b00001000
    BUTTON_START = 0b00000100
    BUTTON_A = 0b00000010
    BUTTON_B = 0b00000001

    panel = GamePadShift(
        DigitalInOut(board.BUTTON_CLOCK),
        DigitalInOut(board.BUTTON_OUT),
        DigitalInOut(board.BUTTON_LATCH),
    )

    has_buttons = has_battery_mon = True
    has_touch = False
    battery_mon = AnalogIn(board.A6)
else:
    has_battery_mon = has_buttons = has_touch = False

# Instantiate slow I2C bus frequency for sensors (50KHz)
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)

# Instantiate CO2 sensor
try:
    scd = adafruit_scd30.SCD30(i2c)
    co2_sensor_exists = True
except:
    print("--- SCD30 SENSOR  ---")
    print("--- NOT CONNECTED ---")
    co2_sensor_exists = False

# co2_sensor_exists = False # ### TEMPORARY SETTING

# Instantiate display, fonts, speaker, and neopixels
display = board.DISPLAY
display.brightness = BRIGHTNESS
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


def update_co2_image_frame(blocking=False, wait_time=3):
    """Acquire SCD-30 data and update the display, returning sensor health flag.
    When blocking = True, the function will wait until the sensor is ready, up
    to 3 seconds (default). When blocking = False, the function will immediately
    return if the sensor data is not available."""
    sensor_data_valid = True  # Used for battery monitoring
    if co2_sensor_exists:
        t0 = time.monotonic()
        while (
            blocking
            and (not scd.data_available)
            and (t0 - time.monotonic() < wait_time)
        ):
            watchdog.fill = RED
            flash_status(interpret(TRANSLATE, "WARMUP"), 0.5)

        if scd.data_available:
            watchdog.fill = YELLOW  # Data acquisition indicator: active
            # Retrieve CO2 sensor data and round value
            sensor_co2 = round(scd.CO2)
            # Get the CO2 quality evaluation descriptor
            (
                sensor_data_valid,
                sensor_co2,
                co2_qual_label.color,
                label,
            ) = co2_ppm_to_quality(sensor_co2)
            # Normalized to 0.0 to 1.0 (for plotting)
            sensor_co2_norm = sensor_co2 / 6000
            # Retrieve humidity data and round value
            sensor_rh = round(scd.relative_humidity)
            # Retrieve temperature data and round value
            sensor_temp = round(scd.temperature)
            if TEMP_UNIT == "F":  # Convert to Fahrenheit if required
                sensor_temp = round(celsius_to_fahrenheit(sensor_temp))

            if sensor_co2 < 6000:
                # Plot quality co2_pointer on scale; adjust fill color for sensor value
                co2_pointer.fill = GRAY
                co2_pointer.y = HEIGHT - int(sensor_co2_norm * HEIGHT)
                co2_pointer_shadow.y = co2_pointer.y
            else:
                # If quality is out-of-range, pin the co2_pointer and show a warning
                co2_pointer.fill = CO2_ALARM[1]
                co2_poointer_shadow.y = co2_pointer.y = 0
                flash_status(interpret(TRANSLATE, "OVERRANGE"), 0.75)

            # Update on-screen values
            co2_qual_label.text = interpret(TRANSLATE, label)
            co2_value.text = str(sensor_co2)
            co2_humid_value.text = str(sensor_rh)
            co2_temp_value.text = str(sensor_temp)
            co2_alarm_value.text = str(CO2_ALARM[0])

            # Draw the CO2 trend chart bars
            for i in range(0, len(co2_trend_chart)):
                co2_trend_group[len(co2_trend_chart) - i - 1].y = (
                    HEIGHT - int(co2_trend_chart[i] * HEIGHT) + 1
                )
                co2_trend_group[len(co2_trend_chart) - i - 1].fill = GRAY
            co2_trend_chart.pop(0)  # remove oldest point from trend
            co2_trend_chart.append(sensor_co2_norm)  # add latest point
    return sensor_data_valid


def read_buttons(joystick=False, timeout=1.0):
    button_pressed = None
    hold_time = 0
    buttons = panel.get_pressed()
    if buttons:
        play_tone(1319, 0.030)  # E6
        if buttons & BUTTON_START:
            button_pressed = "calibrate"
        if buttons & BUTTON_A:
            button_pressed = "a"
        if buttons & BUTTON_B:
            button_pressed = "b"
        if buttons & BUTTON_SELECT:
            button_pressed = "select"
        if buttons & BUTTON_UP:
            button_pressed = "up"
        if buttons & BUTTON_DOWN:
            button_pressed = "down"
        timeout_beep = False
        while buttons:
            buttons = panel.get_pressed()
            time.sleep(0.1)
            hold_time += 0.1
            if hold_time >= timeout and not timeout_beep:
                play_tone(1175, 0.030)  # D6
                timeout_beep = True

    elif joystick:
        if joystick_y.value < 20000:
            button_pressed = "up"
        elif joystick_y.value > 44000:
            button_pressed = "down"
    return button_pressed, hold_time


play_tone(880, 0.1)  # A5

# ### Define the display groups ###
image_group = displayio.Group()
co2_trend_group = displayio.Group()
reference_group = displayio.Group()

# Define co2 trend chart group and points area
co2_trend_chart = []
point_width = int((WIDTH - 28) / 40)  # 40 trend points
for i in range(0, WIDTH - 28, point_width):
    point = Rect(
        x=(WIDTH - 28) - i,
        y=(HEIGHT - 6),
        width=point_width,
        height=HEIGHT * 2,
        fill=None,
        outline=None,
        stroke=0,
    )
    co2_trend_chart.insert(0, HEIGHT)
    co2_trend_group.append(point)
image_group.append(co2_trend_group)

# Add superfluous color margin
cell_height = int(HEIGHT / 32)  # Save memory on large displays
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

# Define CO2 sensor quality scale
if co2_sensor_exists:
    co2_good_scale = Rect(
        x=WIDTH - 22,
        y=HEIGHT - int((1000 / 6000) * HEIGHT),
        width=10,
        height=int(((1000 - 0) / 6000) * HEIGHT) + 3,
        fill=GREEN,
        outline=BLACK,
        stroke=1,
    )
    reference_group.append(co2_good_scale)

    co2_poor_scale = Rect(
        x=WIDTH - 22,
        y=HEIGHT - int((2000 / 6000) * HEIGHT),
        width=10,
        height=int(((2000 - 1000) / 6000) * HEIGHT) + 3,
        fill=YELLOW,
        outline=BLACK,
        stroke=1,
    )
    reference_group.append(co2_poor_scale)

    co2_warning_scale = Rect(
        x=WIDTH - 22,
        y=HEIGHT - int((5000 / 6000) * HEIGHT),
        width=10,
        height=int(((5000 - 2000) / 6000) * HEIGHT) + 3,
        fill=ORANGE,
        outline=BLACK,
        stroke=1,
    )
    reference_group.append(co2_warning_scale)

    co2_danger_scale = Rect(
        x=WIDTH - 22,
        y=HEIGHT - int((6000 / 6000) * HEIGHT),
        width=10,
        height=int(((6000 - 5000) / 6000) * HEIGHT) + 3,
        fill=RED,
        outline=BLACK,
        stroke=1,
    )
    reference_group.append(co2_danger_scale)

    co2_alarm_pointer_shadow = Rect(
        x=WIDTH - 25, y=0, width=14, height=4, fill=RED, outline=BLACK, stroke=1
    )
    co2_alarm_pointer_shadow.y = HEIGHT - int((CO2_ALARM[0] / 6000) * HEIGHT)
    reference_group.append(co2_alarm_pointer_shadow)

    co2_alarm_pointer = Rect(
        x=WIDTH - 25,
        y=HEIGHT - int((CO2_ALARM[0] / 6000) * HEIGHT),
        width=14,
        height=3,
        fill=CO2_ALARM[1],
        outline=BLACK,
        stroke=1,
    )
    reference_group.append(co2_alarm_pointer)

    image_group.append(reference_group)

# Define co2 pointer
co2_pointer_shadow = Rect(
    x=WIDTH - 25, y=HEIGHT + 2, width=14, height=6, fill=None, outline=BLACK, stroke=1
)
image_group.append(co2_pointer_shadow)

co2_pointer = Rect(
    x=WIDTH - 25, y=HEIGHT + 2, width=14, height=5, fill=None, outline=BLACK, stroke=1
)
image_group.append(co2_pointer)

# Define watchdog indicator
watchdog = Rect(x=1, y=1, width=10, height=10, fill=None, outline=YELLOW, stroke=1)
image_group.append(watchdog)

# Define titles, labels, and values for the image group
title_label = Label(font_0, text=interpret(TRANSLATE, SCREEN_TITLE), color=CYAN)
title_label.anchor_point = (0.5, 0)
title_label.anchored_position = ((WIDTH - 20) // 2, 0)
image_group.append(title_label)

status_label = Label(font_0, text=" ", color=None)
status_label.anchor_point = (0.5, 0.5)
status_label.anchored_position = ((WIDTH - 20) // 2, (HEIGHT // 2) + 27)
image_group.append(status_label)

co2_alarm_label = Label(
    font_0, text=interpret(TRANSLATE, CO2_ALARM[2]), color=CO2_ALARM[1]
)
co2_alarm_label.anchor_point = (0, 0)
co2_alarm_label.anchored_position = (5, HEIGHT - 14)
image_group.append(co2_alarm_label)

co2_alarm_value = Label(
    font_0, text=str(CO2_ALARM[0]) if co2_sensor_exists else "----", color=CO2_ALARM[1]
)
co2_alarm_value.anchor_point = (0, 0)
co2_alarm_value.anchored_position = (5, HEIGHT - 28)
image_group.append(co2_alarm_value)

co2_temp_label = Label(font_0, text="°" + TEMP_UNIT, color=CYAN)
co2_temp_label.anchor_point = (0.5, 0)
co2_temp_label.anchored_position = ((WIDTH - 20) // 2, HEIGHT - 14)
image_group.append(co2_temp_label)

co2_temp_value = Label(font_0, text=" " if co2_sensor_exists else "--", color=CYAN)
co2_temp_value.anchor_point = (0.5, 0)
co2_temp_value.anchored_position = ((WIDTH - 20) // 2, HEIGHT - 28)
image_group.append(co2_temp_value)

co2_humid_label = Label(font_0, text="RH", color=CYAN)
co2_humid_label.anchor_point = (1, 0)
co2_humid_label.anchored_position = (WIDTH - 40, HEIGHT - 14)
image_group.append(co2_humid_label)

co2_humid_value = Label(font_0, text=" " if co2_sensor_exists else "--", color=CYAN)
co2_humid_value.anchor_point = (1, 0)
co2_humid_value.anchored_position = (WIDTH - 40, HEIGHT - 28)
image_group.append(co2_humid_value)

co2_qual_label = Label(font_1, text=" ", color=None)
co2_qual_label.anchor_point = (0.5, 0.5)
co2_qual_label.anchored_position = ((WIDTH - 20) // 2, HEIGHT // 4)
image_group.append(co2_qual_label)

co2_label = Label(font_0, text="PPM CO2", color=BLUE)
co2_label.anchor_point = (0.5, 0)
co2_label.anchored_position = ((WIDTH - 20) // 2, 4 + (HEIGHT // 2))
image_group.append(co2_label)

co2_value = Label(font_1, text=" " if co2_sensor_exists else "---", color=WHITE)
co2_value.anchor_point = (0.5, 1.0)
co2_value.anchored_position = ((WIDTH - 20) // 2, HEIGHT // 2)
image_group.append(co2_value)


# ###--- PRIMARY PROCESS SETUP ---###
# Activate display and play welcome tones
display.show(image_group)
if co2_sensor_exists:
    scd.reset()  # Reset sensor and set acquisition interval
    scd.measurement_interval = SENSOR_INTERVAL
# Wait for sensor data and display
sensor_valid = update_co2_image_frame(blocking=True)

play_tone(440, 0.1)  # A4
play_tone(880, 0.1)  # A5

if not co2_sensor_exists:
    flash_status(interpret(TRANSLATE, "NO CO2 SENSOR"), 2.0)

# ###--- PRIMARY PROCESS LOOP ---###
t0 = time.monotonic()  # Reset sensor interval timer
while True:
    if has_buttons:
        button_pressed, hold_time = read_buttons()
        if button_pressed == "calibrate":  # Recalibrate mode selected (start)
            if hold_time >= 1.0:  # long press
                if co2_sensor_exists:
                    flash_status(interpret(TRANSLATE, "CALIBRATE"), 0.5)
                    adafruit_scd30.forced_recalibration_reference = 400
                else:
                    flash_status(interpret(TRANSLATE, "NO CO2 SENSOR"), 0.5)
                play_tone(440, 0.1)  # A4
        if button_pressed == "select":  # Toggle temperature units
            if hold_time >= 1.0:  # long press
                flash_status(interpret(TRANSLATE, "TEMPERATURE"), 0.5)
                if TEMP_UNIT == "F":
                    TEMP_UNIT = "C"
                else:
                    TEMP_UNIT = "F"
                co2_temp_label.text = "°" + TEMP_UNIT
                play_tone(440, 0.1)  # A4
        if button_pressed == "a":  # Toggle language
            if hold_time >= 1.0:  # long press
                flash_status(interpret(TRANSLATE, "LANGUAGE"), 0.5)
                TRANSLATE = not TRANSLATE
                title_label.text = interpret(TRANSLATE, SCREEN_TITLE)
                co2_alarm_label.text = interpret(TRANSLATE, CO2_ALARM[2])
                play_tone(440, 0.1)  # A4
                if TRANSLATE:
                    flash_status(interpret(True, "ENGLISH"), 0.5)
                else:
                    flash_status("ENGLISH", 0.5)

    if time.monotonic() - SENSOR_INTERVAL > t0:
        # If available, acquire sensor data and update display
        sensor_valid = update_co2_image_frame()
        t0 = time.monotonic()
    else:
        watchdog.fill = BLUE
        watchdog.x = int(((time.monotonic() - t0) / SENSOR_INTERVAL) * 10) - 10
        watchdog.y = watchdog.x

    # If CO2 alarm threshold is reached, flash NeoPixels, ALARM status, and play alarm tone
    if co2_sensor_exists:
        if co2_value.text != " " and float(co2_value.text) >= CO2_ALARM[0]:
            flash_status(interpret(TRANSLATE, "ALARM"), 0.75)
            if has_neopixel:
                pixels.fill(RED)
            play_tone(880, 0.015)  # A5
            if has_neopixel:
                pixels.fill(BLACK)

    if has_battery_mon:
        """Warns when battery voltage is low and the sensor data is potentially
        invalid (measured value is less than 100). The 3.3-volt threshold is an
        approximation since an individual board's battery monitoring circuitry
        can vary +/-10% due to internal voltage divider resistor tolerance."""
        battery_volts = round(battery_mon.value * 6.6 / 0xFFF0, 2)
        if (not sensor_valid) and battery_volts < 3.3:
            play_tone(880, 0.030)  # A5
            flash_status(interpret(TRANSLATE, "LOW BATTERY"), 1)
            flash_status(str(battery_volts) + " volts", 1)
