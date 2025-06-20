import ctypes
import os
from text_editor.editor import add_layout_to_image

def set_wallpaper(image_path):
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)

if __name__ == '__main__':
    output_path = add_layout_to_image(
        image_path = "assets/images/base_image4.jpg",
        margin = 50,
        line_width = 3,
        font_path = "assets/fonts/Montserrat-VariableFont_wght.ttf",
        font_size = 24,
        font_color = (255, 255, 255),
    )
    # set_wallpaper(output_path)

