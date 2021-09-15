# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_funhome.py
# 2021-09-15 v1.0.1

import board
import time
from digitalio import DigitalInOut, Pull, Direction
import displayio
from adafruit_display_shapes.rect import Rect


class Buttons:
    def __init__(self):
        """Instantiate the air monitor button decoder for the
        FunHouse device. Builds displayio button group."""

        self._timeout = 1
        self._WIDTH = board.DISPLAY.width
        self._HEIGHT = board.DISPLAY.height

        # Define and instantiate front panel buttons
        self._BUTTON_TEMPERATURE = DigitalInOut(board.BUTTON_DOWN)  # Select
        self._BUTTON_TEMPERATURE.direction = Direction.INPUT
        self._BUTTON_TEMPERATURE.pull = Pull.DOWN
        self._BUTTON_CALIBRATE = DigitalInOut(board.BUTTON_SELECT)  # Up
        self._BUTTON_CALIBRATE.direction = Direction.INPUT
        self._BUTTON_CALIBRATE.pull = Pull.DOWN
        self._BUTTON_LANGUAGE = DigitalInOut(board.BUTTON_UP)  # Down
        self._BUTTON_LANGUAGE.direction = Direction.INPUT
        self._BUTTON_LANGUAGE.pull = Pull.DOWN

        # Build displayio button group
        self._button_group = displayio.Group()
        self.language_button = Rect(
            x=1,
            y=1,
            width=self._WIDTH - 20,
            height=int(self._HEIGHT * 0.25),
            fill=None,
            outline=0x000000,
            stroke=1,
        )
        self._button_group.append(self.language_button)
        self.language_button.outline = None

        self.calibrate_button = Rect(
            x=int((self._WIDTH - 20) * 0.25),
            y=int(self._HEIGHT * 0.33),
            width=int((self._WIDTH - 20) / 2),
            height=int(self._HEIGHT * 0.33),
            fill=None,
            outline=0x000000,
            stroke=1,
        )
        self._button_group.append(self.calibrate_button)
        self.calibrate_button.outline = None

        self.temperature_button = Rect(
            x=1,
            y=int(self._HEIGHT * 0.75) - 1,
            width=self._WIDTH - 20,
            height=int(self._HEIGHT * 0.25),
            fill=None,
            outline=0x000000,
            stroke=1,
        )
        self._button_group.append(self.temperature_button)
        self.temperature_button.outline = None
        return

    @property
    def button_display_group(self):
        """Displayio button group."""
        return self._button_group

    @property
    def timeout(self):
        """Button timeout duration setting."""
        return self._timeout

    @timeout.setter
    def timeout(self, hold_time=1.0):
        """Select timeout duration value in seconds, positive float value."""
        if hold_time < 0 or hold_time >= 10:
            "Invalid button timeout duration value. Must be between 0 and 10 seconds."
            return
        self._timeout = hold_time
        return

    def read_buttons(self):
        self._button_pressed = None
        self._hold_time = 0

        if self._BUTTON_CALIBRATE.value:
            self._button_pressed = "calibrate"
            self.calibrate_button.outline = 0x0000FF
            while self._BUTTON_CALIBRATE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    self.calibrate_button.outline = 0x00FF00
        if self._BUTTON_LANGUAGE.value:
            self._button_pressed = "language"
            self.language_button.outline = 0x0000FF
            while self._BUTTON_LANGUAGE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    self.language_button.outline = 0x00FF00
        if self._BUTTON_TEMPERATURE.value:
            self._button_pressed = "temperature"
            self.temperature_button.outline = 0x0000FF
            while self._BUTTON_TEMPERATURE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    self.temperature_button.outline = 0x00FF00
        self.calibrate_button.outline = None
        self.language_button.outline = None
        self.temperature_button.outline = None
        return self._button_pressed, self._hold_time
