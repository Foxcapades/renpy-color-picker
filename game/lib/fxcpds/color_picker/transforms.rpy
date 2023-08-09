transform _color_picker_slider:
    shader "fxcpds.slider"

transform _color_picker_square(tr):
    shader "fxcpds.color_block"
    u_top_right_rgb _color_picker_normalize_rgb(tr.rgb)
