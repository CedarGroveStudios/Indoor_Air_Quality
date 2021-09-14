# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_pybadge.py
# 2021-09-14 v1.0.0

import board
import time
from digitalio import DigitalInOut
from analogio import AnalogIn
import displayio
from adafruit_display_shapes.rect import Rect
from gamepadshift import GamePadShift
from simpleio import tone

# from keypad import ShiftRegisterKeys  # CircuitPython v7.0.0
# https://circuitpython.readthedocs.io/en/latest/shared-bindings/keypad/index.html#module-keypad


class Buttons:
    def __init__(self, disp_height=128, disp_width=160):
        """Instantiate the air monitor button decoder for the
        PyBadge/PyGamer/EdgeBadge device. Returns displayio button group."""

        self._timeout = 1

        # Define and instantiate front panel buttons
        self._BUTTON_TEMPERATURE = 0b00001000  # Select
        self._BUTTON_CALIBRATE = 0b00000100  # start
        self._BUTTON_LANGUAGE = 0b00000010  # A

        self._panel = GamePadShift(
            DigitalInOut(board.BUTTON_CLOCK),
            DigitalInOut(board.BUTTON_OUT),
            DigitalInOut(board.BUTTON_LATCH),
        )

        # Build displayio button group
        self._button_group = displayio.Group()
        self.language_button = Rect(
            x=0,
            y=0,
            width=disp_width,
            height=int(disp_height * 0.25),
            fill=None,
            outline=0x000000,
            stroke=1,
        )
        self._button_group.append(self.language_button)
        self.language_button.outline = None

        self.calibrate_button = Rect(
            x=0,
            y=int(disp_height * 0.25),
            width=disp_width,
            height=int(disp_height * 0.50),
            fill=None,
            outline=0x000000,
            stroke=1,
        )
        self._button_group.append(self.calibrate_button)
        self.calibrate_button.outline = None

        self.temperature_button = Rect(
            x=0,
            y=int(disp_height * 0.75),
            width=disp_width,
            height=int(disp_height * 0.25),
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
        self._buttons = self._panel.get_pressed()
        if self._buttons:
            tone(board.A0, 1319, 0.030)  # E6
            if self._buttons & self._BUTTON_CALIBRATE:
                self._button_pressed = "calibrate"
                self.calibrate_button.outline = 0x0000FF
            if self._buttons & self._BUTTON_LANGUAGE:
                self._button_pressed = "language"
                self.language_button.outline = 0x0000FF
            if self._buttons & self._BUTTON_TEMPERATURE:
                self._button_pressed = "temperature"
                self.temperature_button.outline = 0x0000FF
            self._timeout_beep = False
            while self._buttons:
                self._buttons = self._panel.get_pressed()
                time.sleep(0.1)
                self._hold_time += 0.1
                if self._hold_time >= self._timeout and not self._timeout_beep:
                    tone(board.A0, 1175, 0.030)  # D6
                    self._timeout_beep = True
            self.calibrate_button.outline = None
            self.language_button.outline = None
            self.temperature_button.outline = None
        return self._button_pressed, self._hold_time
