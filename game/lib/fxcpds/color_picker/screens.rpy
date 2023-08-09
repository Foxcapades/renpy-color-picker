screen color_picker:
    default picker = ColorPicker(400, 400)

    frame:
        style "_color_picker_background_overlay"
        xfill True
        yfill True

        frame:
            style "_color_picker_pane"
            xcenter 0.5
            ycenter 0.5

            hbox:
                use _color_picker_left_pane(picker)
                use _color_picker_right_pane(picker)


screen _color_picker_left_pane(picker):
    frame:
        style "_color_picker_left_pane"
        hbox:
            spacing 5
            xcenter 0.5
            ycenter 0.5

            add picker

            vbar:
                value picker.rotation
                xysize (25, 400)
                range 359
                base_bar At(Transform('#fff', xysize=(25, 400)), _color_picker_slider())
                thumb Transform("lib/fxcpds/color_picker/slider.png")
                thumb_offset 4
                changed picker.set_rotation


screen _color_picker_right_pane(picker):
    default selected_tab = StringContainer("RGB")

    vbox:
        style "_color_picker_right_pane"

        spacing 5

        vbox:
            frame:
                style "_color_picker_tab_bar"
                hbox:
                    use _color_picker_tab("HSL", selected_tab)
                    use _color_picker_tab("HSV", selected_tab)
                    use _color_picker_tab("RGB", selected_tab)

            frame:
                style "_color_picker_right_pane_body"

                vbox:
                    spacing 10

                    use _color_picker_right_header(picker)

                    if selected_tab.value == "HSL":
                        use _color_picker_hsl_pane(picker)
                    elif selected_tab.value == "HSV":
                        use _color_picker_hsv_pane(picker)
                    elif selected_tab.value == "RGB":
                        use _color_picker_rgb_pane(picker)

                    use _color_picker_right_footer(picker)


screen _color_picker_tab(name, selected_tab):
    vbox:
        button:
            if selected_tab.value == name:
                style "_color_picker_tab_top_selected"
            else:
                style "_color_picker_tab_top_idle"

            text name:
                style "_color_picker_tab_text"

            action Function(selected_tab.set_value, name)

        textbutton name:
            if selected_tab.value == name:
                style "_color_picker_tab_button_selected"
            else:
                style "_color_picker_tab_button_idle"

            action Function(selected_tab.set_value, name)


screen _color_picker_hsl_pane(picker):
    vbox:
        spacing 10
        vbox:
            text "Hue":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 359
                value picker.hsl.hue
                changed _color_picker_hsl_bar_setter(picker, 'h')
        vbox:
            text "Saturation":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 1.0
                value picker.hsl.saturation
                changed _color_picker_hsl_bar_setter(picker, 's')
        vbox:
            text "Lightness":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 1.0
                value picker.hsl.lightness
                changed _color_picker_hsl_bar_setter(picker, 'l')


screen _color_picker_hsv_pane(picker):
    vbox:
        spacing 10
        vbox:
            text "Hue":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 359
                value picker.hsv.hue
                changed _color_picker_hsv_bar_setter(picker, 'h')
        vbox:
            text "Saturation":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 1.0
                value picker.hsv.saturation
                changed _color_picker_hsv_bar_setter(picker, 's')
        vbox:
            text "Value":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 1.0
                value picker.hsv.value
                changed _color_picker_hsv_bar_setter(picker, 'v')


screen _color_picker_rgb_pane(picker):
    vbox:
        spacing 10
        vbox:
            text "Red":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 255
                value picker.rgb.red
                changed _color_picker_rgb_bar_setter(picker, 'r')
        vbox:
            text "Green":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 255
                value picker.rgb.green
                changed _color_picker_rgb_bar_setter(picker, 'g')
        vbox:
            text "Blue":
                style "_color_picker_bar_title"
            bar:
                ysize 25
                range 255
                value picker.rgb.blue
                changed _color_picker_rgb_bar_setter(picker, 'b')


screen _color_picker_right_header(picker):
    default hex_input = HexInputValue(picker)

    hbox:
        spacing 5

        text "Hex"

        null:
            width 25

        button:
            style "_color_picker_hex_button"
            key_events True
            ycenter 0.5

            input:
                style "_color_picker_hex_input"
                value hex_input
                prefix '#'
                length 6
                copypaste True

            action hex_input.Toggle()


screen _color_picker_right_footer(picker):
    default preview = DynamicDisplayable(_color_picker_preview_cb, picker=picker)

    hbox:
        style "_color_picker_right_pane_footer"

        add preview:
            xsize 78
            ysize 78

        textbutton "Done":
            style "_color_picker_done_button"
            action Return(picker.color.hex)
