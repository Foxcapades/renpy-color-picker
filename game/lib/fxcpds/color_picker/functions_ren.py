from fox_color_ren import FoxHSV, FoxColor
from displayable_ren import ColorPicker

"""renpy
init -2 python:
"""

def _color_picker_preview_cb(st: float, at: float, picker: ColorPicker):
    return (picker.color.hex, 0.01)

def _color_picker_normalize_rgb(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    return (rgb[0]/255, rgb[1]/255, rgb[2]/255)
