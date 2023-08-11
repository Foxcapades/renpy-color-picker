init python:

    def bg_callback(st, at):
        return (Solid(bg_color), None)

image bg solid = DynamicDisplayable(bg_callback)

default bg_color = "#9cb9cb"

define e = Character("Eileen", who_prefix="{color=[bg_color]}", who_suffix="{/color}")

label start:

    scene bg solid

    while True:
        e "Pick a color."

        window hide
        $ bg_color = renpy.call_screen("color_picker", bg_color)
        window show

        e "You selected the color {color=[bg_color]}[bg_color]{/color}"

    return
