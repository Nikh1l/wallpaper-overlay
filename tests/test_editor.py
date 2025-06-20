import sys
import os

# Add the parent directory (Wallpaper/) to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
from text_editor.editor import add_text_to_image

def test_add_text_to_image():
    output_path = "output/test.png"
    add_text_to_image(
        image_path="assets/images/base_image.jpg",
        text="Test",
        font_path="assets/fonts/Cookie-Regular.ttf",
        font_size=20,
        position=(10, 10),
        output_path=output_path
    )
    assert os.path.exists(output_path)