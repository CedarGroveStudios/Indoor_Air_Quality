# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_clue.py
# 2021-09-14 v1.0.1

import board
import time
from digitalio import DigitalInOut, Pull, Direction
from simpleio import tone

class Buttons:
    def __init__(self):
        """Instantiate the air monitor button decoder for the
        CLUE device."""

        self._timeout = 1
        self._WIDTH = board.DISPLAY.width
        self._HEIGHT = board.DISPLAY.height

        # Define and instantiate front panel buttons
        self._BUTTON_TEMPERATURE = DigitalInOut(board.BUTTON_B)  # B
        self._BUTTON_TEMPERATURE.direction = Direction.INPUT
        self._BUTTON_TEMPERATURE.pull = Pull.UP
        self._BUTTON_CALIBRATE = DigitalInOut(board.D3)  # pin 3
        self._BUTTON_CALIBRATE.direction = Direction.INPUT
        self._BUTTON_CALIBRATE.pull = Pull.UP
        self._BUTTON_LANGUAGE = DigitalInOut(board.BUTTON_A)  # A
        self._BUTTON_LANGUAGE.direction = Direction.INPUT
        self._BUTTON_LANGUAGE.pull = Pull.UP

        self._button_group = False
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

        if not self._BUTTON_CALIBRATE.value:
            tone(board.A0, 1319, 0.030)  # E6
            self._button_pressed = "calibrate"
            print(self._button_pressed)
            while not self._BUTTON_CALIBRATE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    tone(board.A0, 1175, 0.030)  # D6
        if not self._BUTTON_LANGUAGE.value:
            tone(board.A0, 1319, 0.030)  # E6
            self._button_pressed = "language"
            print(self._button_pressed)
            while not self._BUTTON_LANGUAGE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    tone(board.A0, 1175, 0.030)  # D6
        if not self._BUTTON_TEMPERATURE.value:
            tone(board.A0, 1319, 0.030)  # E6
            self._button_pressed = "temperature"
            print(self._button_pressed)
            while not self._BUTTON_TEMPERATURE.value:
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout:
                    tone(board.A0, 1175, 0.030)  # D6
        return self._button_pressed, self._hold_time
