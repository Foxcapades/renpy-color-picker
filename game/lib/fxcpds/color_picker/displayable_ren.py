from renpy import At, Fixed, Image, InputValue, Transform  # type: ignore
import renpy  # type: ignore
from transforms import _color_picker_square  # type: ignore
from fox_hex_utils_ren import fox_hex_is_valid
from fox_color_ren import FoxHSV, hex_to_fox_rgb

"""renpy
init python:
"""

import pygame


class ColorPicker(renpy.Displayable):

    WHITE = FoxHSV.white()
    BLACK = FoxHSV.black()
    RED = FoxHSV(0, 1.0, 1.0)
    SELECT = Image("lib/fxcpds/color_picker/selector.png")

    def __init__(self, width: int, height: int, **kwargs) -> None:
        super(ColorPicker, self).__init__(**kwargs)

        self.color = self.RED.clone()

        self._width = width
        self._height = height
        self._picker = Transform('#fff', xysize=(width, height))
        self._dragged = False

    @property
    def rotation(self) -> int:
        return self.color.hue

    def set_rotation(self, rotation: int) -> None:
        self.color.set_hue(rotation)
        renpy.restart_interaction()

    def render(self, width, height, st, at) -> renpy.Render:
        view = renpy.Render(self._width, self._height)
        picker = At(self._picker, _color_picker_square(self.RED.rotate_hue_by_degrees(self.rotation)))
        select = Transform(
            self.SELECT,
            anchor=(0.5, 0.5),
            xpos=self.color.saturation,
            ypos=1.0 - self.color.value,
        )

        pane = Fixed(picker, select, xysize=(self._width, self._height))
        rend = renpy.render(pane, self._width, self._height, st, at)

        view.blit(rend, (0, 0))

        renpy.redraw(self, 0.01)

        return view

    def event(self, ev: pygame.event.Event, x: float, y: float, st: float) -> None:
        # Figure out where the heck the mouse cursor is relative to our color
        # picker square.
        x_percent = x / self._width
        y_percent = y / self._height
        in_square = 0.0 <= x_percent <= 1.0 and 0.0 <= y_percent <= 1.0
        y_percent = 1.0 - y_percent

        # Check if we are dragging and update our stored x/y position for the
        # mouse cursor if it is within the square.
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and in_square:
            self._dragged = True
            self.color.set_saturation(self._clamp(x_percent))
            self.color.set_value(self._clamp(y_percent))
        elif ev.type == pygame.MOUSEMOTION and self._dragged:
            self.color.set_saturation(self._clamp(x_percent))
            self.color.set_value(self._clamp(y_percent))
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self._dragged = False
            renpy.restart_interaction()

        return None

    def visit(self) -> list[Image]:
        return [self.SELECT]

    def update_position(self):
        h, s, v = self.color.hsv
        self.rotation = h
        self._xpos = s
        self._ypos = 1.0 - v

    @staticmethod
    def _clamp(percent: float) -> float:
        if percent > 1.0:
            return 1.0
        elif percent < 0.0:
            return 0.0
        else:
            return percent


class HexInputValue(InputValue):
    def __init__(self, picker: ColorPicker):
        self.default = False
        self._picker = picker
        self._last   = picker.color.hex[1:]
        self._value  = self._last

    def get_text(self) -> str:
        hex = self._picker.color.hex[1:]

        if hex == self._last:
            return self._value
        else:
            self._last = self._value = hex
            return hex

    def set_text(self, text: str):
        if fox_hex_is_valid(text):
            self._value = text

            if len(text) == 6:
                self._picker.color = hex_to_fox_rgb('#' + text).to_hsv()

        renpy.restart_interaction()
