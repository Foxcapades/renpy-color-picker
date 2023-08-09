##
## Tabs Style
##

style _color_picker_tab_text:
    size 32

style _color_picker_tab_bar:
    background "black"
    xsize 300

style _color_picker_tab_button:
    padding (10, 3)

style _color_picker_tab_button_idle:
    is _color_picker_tab_button
    background "black"

style _color_picker_tab_button_idle_text:
    is _color_picker_tab_text
    color gui.idle_color

style _color_picker_tab_button_selected:
    is _color_picker_tab_button
    background "#333333"

style _color_picker_tab_button_selected_text:
    is _color_picker_tab_text
    color gui.selected_color

style _color_picker_tab_top:
    padding (10, 0)
    ysize 5

style _color_picker_tab_top_idle:
    is _color_picker_tab_top
    background gui.muted_color

style _color_picker_tab_top_idle_text:
    is _color_picker_tab_text

style _color_picker_tab_top_selected:
    is _color_picker_tab_top
    background gui.accent_color

style _color_picker_tab_top_selected_text:
    is _color_picker_tab_text


##
## Misc
##

style _color_picker_background_overlay:
    background "#0000007f"

style _color_picker_pane:
    background None

##
## Hex Input
##
style _color_picker_hex_button:
    background '#fff'
    xsize 150

style _color_picker_hex_input:
    color gui.accent_color
    size 32


##
## Right Pane
##

style _color_picker_right_pane:
    xsize 300

style _color_picker_right_pane_body:
    background "#333333"
    padding (0, 5, 5, 5)

style _color_picker_bar_title:
    size 32

style _color_picker_right_pane_footer:
    ysize 83
    xsize 295

style _color_picker_done_button:
    xanchor 1.0
    xpos 1.0
    yanchor 1.0
    ypos 1.0

style _color_picker_done_button_text:
    color gui.idle_color
    hover_color gui.hover_color

##
## Left Pane
##

style _color_picker_left_pane:
    background "#333333"
    padding (5, 5)
