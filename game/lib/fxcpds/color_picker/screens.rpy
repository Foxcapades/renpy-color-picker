default _color_picker_selected_tab = "RGB"

style _color_picker_background_overlay:
    background "#0000007f"

style _color_picker_pane:
    background "#333333"
    padding (5, 5)

style _color_picker_hex_button:
    background '#fff'
    xsize 100

style _color_picker_hex_input:
    color gui.accent_color
    size 20


screen color_picker:
    default picker = ColorPicker(300, 300)
    default preview = DynamicDisplayable(_color_picker_preview_cb, picker=picker)
    default hex_input = HexInputValue(picker)

    frame:
        style "_color_picker_background_overlay"
        xfill True
        yfill True

        frame:
            style "_color_picker_pane"
            xcenter 0.5
            ycenter 0.5

            hbox:
                spacing 5
                xcenter 0.5
                ycenter 0.5

                add picker

                vbar:
                    value picker.rotation
                    xysize (25, 300)
                    range 359
                    base_bar At(Transform('#fff', xysize=(25, 300)), _color_picker_slider())
                    thumb Transform("lib/fxcpds/color_picker/slider.png")
                    thumb_offset 4
                    changed picker.set_rotation

                vbox:
                    spacing 5
                    add preview:
                        xsize 100
                        ysize 100

                    button:
                        style "_color_picker_hex_button"
                        key_events True

                        input:
                            style "_color_picker_hex_input"
                            value hex_input
                            prefix '#'
                            length 6
                            copypaste True

                        action hex_input.Toggle()


