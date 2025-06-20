# Wallpaper Calendar Overlay

This project generates a custom desktop wallpaper by overlaying a calendar (with the current date highlighted) on top of any background image. The result is a visually appealing, always-up-to-date wallpaper for your Windows desktop.

## Purpose
- **Personal Productivity:** See the current date at a glance, right on your desktop.
- **Aesthetics:** Use any image as your wallpaper background, with a stylish calendar overlay.
- **Automation:** Automatically update your wallpaper every day with the correct date circled.

## Features
- Overlay a calendar for the current month on any image.
- The current date is highlighted with a hand-drawn style encircle (using a PNG overlay for best visual quality).
- Customizable fonts and colors.
- Output is always 1920x1080 (HD) for consistency.
- Designed for easy automation on Windows (e.g., with Task Scheduler).

## How to Use

### 1. Prerequisites
- Python 3.8+
- Install dependencies:
  ```bash
  pip install pillow
  ```

### 2. Prepare Your Assets
- Place your background image(s) in `assets/images/` (e.g., `base_image.jpg`).
- Place your encircle PNG (e.g., `encircle.png`) in `assets/images/`.
- Place your preferred font(s) in `assets/fonts/`.

### 3. Run the Script
Edit `main.py` to set your image, font, and output path as needed. Then run:
```bash
python main.py
```
The output image will be saved in the `output/` directory.

### 4. Set as Desktop Wallpaper (Windows)
The script can automatically set the generated image as your wallpaper. If not, you can set it manually:
- Right-click the output image and choose "Set as desktop background".

To automate this daily:
- Use Windows Task Scheduler to run `python main.py` every day (at logon or a set time).

## Customization
- **Change the encircle color:** Edit the `desired_color` variable in `text_editor/editor.py`.
- **Change fonts or background:** Replace files in `assets/fonts/` or `assets/images/`.
- **Change calendar style:** Edit the drawing logic in `text_editor/editor.py`.

## Project Structure
- `main.py` — Entry point for generating and applying the wallpaper.
- `text_editor/editor.py` — Core logic for drawing overlays and calendar.
- `assets/` — Fonts and images used for overlays.
- `output/` — Generated wallpapers.

## License
This project is for personal use. Encircle PNG and fonts should be used according to their respective licenses.

---
Enjoy your always-up-to-date, beautiful desktop wallpaper!

