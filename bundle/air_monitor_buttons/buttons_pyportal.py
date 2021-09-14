# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_pyportal.py
# 2021-09-14 v1.0.1

import board
import time

# from digitalio import DigitalInOut
# from analogio import AnalogIn
import displayio
from adafruit_button import Button
import adafruit_touchscreen
from simpleio import tone


class Buttons:
    def __init__(self, disp_height=128, disp_width=160):
        """Instantiate the air monitor buttons for PyPortal devices."""

        self._timeout = 1
        self._WIDTH = board.DISPLAY.width
        self._HEIGHT = board.DISPLAY.height

        self._ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_XL,
            board.TOUCH_XR,
            board.TOUCH_YD,
            board.TOUCH_YU,
            calibration=((5200, 59000), (5800, 57000)),
            size=(self._WIDTH, self._HEIGHT),
        )

        # Build displayio button group #
        self._buttons = []
        self._button_group = displayio.Group()

        self.language_button = Button(
            x=1,
            y=1,
            height=int(self._HEIGHT * 0.25),
            width=self._WIDTH - 20,
            style=Button.RECT,
            fill_color=None,
            outline_color=0x000000,
            name="language",
            selected_fill=None,
            selected_outline=0x0000FF,
        )
        self._button_group.append(self.language_button)
        self._buttons.append(self.language_button)
        self.language_button.outline_color = None

        self.calibrate_button = Button(
            x=int((self._WIDTH - 20) * 0.25),
            y=int(self._HEIGHT * 0.33),
            height=int(self._HEIGHT * 0.33),
            width=int((self._WIDTH - 20) / 2),
            style=Button.RECT,
            fill_color=None,
            outline_color=0x000000,
            name="calibrate",
            selected_fill=None,
            selected_outline=0x0000FF,
        )
        self._button_group.append(self.calibrate_button)
        self._buttons.append(self.calibrate_button)
        self.calibrate_button.outline_color = None

        self.temperature_button = Button(
            x=1,
            y=int(self._HEIGHT * 0.75),
            height=int(self._HEIGHT * 0.25) - 1,
            width=self._WIDTH - 20,
            style=Button.RECT,
            fill_color=None,
            outline_color=0x000000,
            name="temperature",
            selected_fill=None,
            selected_outline=0x0000FF,
        )
        self._button_group.append(self.temperature_button)
        self._buttons.append(self.temperature_button)
        self.temperature_button.outline_color = None
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
        self._touch = self._ts.touch_point
        if self._touch:
            for self._button in self._buttons:
                if self._button.contains(self._touch):
                    self._button.selected = True
                    tone(board.A0, 1319, 0.030)  # E6
                    self._button_pressed = self._button.name
                    self._timeout_beep = False
                    while self._ts.touch_point:
                        time.sleep(0.1)
                        self._hold_time += 0.1
                        if self._hold_time >= self._timeout and not self._timeout_beep:
                            tone(board.A0, 1175, 0.030)  # D6
                            self._timeout_beep = True
                    self._button.selected = False
        return self._button_pressed, self._hold_time
