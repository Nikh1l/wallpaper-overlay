from PIL import Image, ImageDraw, ImageFont
import os
import calendar
import datetime
import random
import math

def add_layout_to_image(image_path, margin, line_width, font_path, font_size, output_path = "output/result.png", font_color=(0, 0, 0)):
    # Load image
    image = Image.open(image_path).convert('RGBA')
    # Standardize to 1920x1080 for consistent layout
    target_size = (1920, 1080)
    if image.size != target_size:
        image = image.resize(target_size, Image.LANCZOS)
    output_path = "output/" + str(image_path.split("/")[-1].split(".")[0]) + ".png"
    draw = ImageDraw.Draw(image)
    width, height = image.size

    spacing = margin
    total_inner_spacing = 2 * spacing
    total_outer_margin = 2 * margin

    # Define width ratios for columns: [left, center, right]
    ratios = [1, 2, 1]
    total_ratio = sum(ratios)
    available_width = width - total_outer_margin - total_inner_spacing
    column_widths = [int(available_width * r / total_ratio) for r in ratios]

    # Calculate x positions for each column
    column_x = [margin]
    for i in range(1, 3):
        prev_x = column_x[i-1]
        prev_w = column_widths[i-1]
        column_x.append(prev_x + prev_w + spacing)

    column_height = height - 2 * margin
    font = ImageFont.truetype(font_path, font_size)
    try:
        font = ImageFont.truetype(
            "assets/fonts/Montserrat-VariableFont_wght.ttf",
            font.size,
        )
        # print(font.get_variation_names())
        font.set_variation_by_name('Regular')
    except Exception as e:
        print("Using default font as custom font loading failed with exception:", e)

    for index in range(3):
        if index == 2:
            # Split the third column into two rows
            half_height = column_height // 2
            # Top row
            image = draw_column(image, index, column_x[index], margin, column_widths[index], half_height, font, font_color, row=0)
            # Bottom row
            image = draw_column(image, index, column_x[index], margin + half_height, column_widths[index], column_height - half_height, font, font_color, row=1)
        else:
            image = draw_column(image, index, column_x[index], margin, column_widths[index], column_height, font, font_color)

    # Save Output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path


def draw_column(base_image, index, x, y, width, height, font, font_color, row=None):
    rect_left, rect_top, rect_width, rect_height, corner_radius = get_column_attributes(
        index, 20, x, y, width, height, row=row)

    rounded_rect = get_rounded_rect(4, rect_width, rect_height, corner_radius)
    overlay = overlay_rect_paste(base_image.size, rounded_rect, rect_left, rect_top)

    # Draw calendar in column 2, row 0
    if index == 2 and row == 0:
        draw_calendar_on_overlay(overlay, rect_left, rect_top, rect_width, rect_height, font, font_color)

    return Image.alpha_composite(base_image, overlay)


def draw_calendar_on_overlay(overlay, rect_left, rect_top, rect_width, rect_height, font, font_color):
    draw = ImageDraw.Draw(overlay)
    today = datetime.date.today()
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(today.year, today.month))
    month_matrix = [month_days[i:i+7] for i in range(0, len(month_days), 7)]
    week_days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

    # Add padding inside the calendar box
    pad_x = int(rect_width * 0.07)
    pad_y = int(rect_height * 0.07)
    cal_left = rect_left + pad_x
    cal_top = rect_top + pad_y
    cal_width = rect_width - 2 * pad_x
    cal_height = rect_height - 2 * pad_y

    # Calculate cell size
    cell_w = cal_width // 7
    cell_h = cal_height // (len(month_matrix) + 2)  # +2 for month name and weekdays
    x0 = cal_left
    y0 = cal_top

    # Draw month name
    month_name = today.strftime('%B %Y')
    bbox = font.getbbox(month_name)
    text_w = bbox[2] - bbox[0]
    draw.text((x0 + (cal_width - text_w)//2, y0), month_name, font=font, fill=font_color)
    y0 += cell_h

    # Draw weekdays
    for i, wd in enumerate(week_days):
        bbox = font.getbbox(wd)
        text_w = bbox[2] - bbox[0]
        draw.text((x0 + i*cell_w + (cell_w-text_w)//2, y0), wd, font=font, fill=font_color)
    y0 += cell_h

    # Load encircle image and optionally tint it
    try:
        encircle_img = Image.open("assets/images/encircle.png").convert("RGBA")
        # Change color here: e.g., to blue (0, 102, 255)
        desired_color = (200, 0, 0)  # Change this to any RGB value you want
        r, g, b, a = encircle_img.split()
        # Create a new image filled with the desired color and use the alpha channel as mask
        color_img = Image.new("RGBA", encircle_img.size, desired_color + (0,))
        encircle_img = Image.composite(color_img, encircle_img, a)
        encircle_img.putalpha(a)
    except Exception as e:
        encircle_img = None
        print("Could not load encircle image:", e)

    # Draw days and overlay encircle image on today
    for week in month_matrix:
        for i, day in enumerate(week):
            if day == 0:
                continue
            day_str = str(day)
            bbox = font.getbbox(day_str)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            cx = x0 + i*cell_w + cell_w//2
            cy = y0 + cell_h//2
            draw.text((cx - text_w//2, cy - text_h//2), day_str, font=font, fill=font_color)
            if day == today.day and encircle_img is not None:
                # Resize encircle image to fit cell
                scale = min(cell_w, cell_h) / max(encircle_img.width, encircle_img.height) * 1.5
                new_size = (int(encircle_img.width * scale), int(encircle_img.height * scale))
                encircle_resized = encircle_img.resize(new_size, Image.LANCZOS)
                # Random rotation for natural effect
                angle = random.uniform(-18, 18)
                encircle_rotated = encircle_resized.rotate(angle, expand=True, resample=Image.BICUBIC)
                # Calculate position to center the encircle image
                ex = int(cx - encircle_rotated.width // 2)
                ey = int(cy - encircle_rotated.height // 2)
                overlay.paste(encircle_rotated, (ex, ey + 5), encircle_rotated)
        y0 += cell_h


def get_column_attributes(index, padding, x, y, width, height, row=None):
    rect_top = y
    corner_radius = 40
    rect_bottom = 0
    rect_left = 0
    rect_right = 0

    if index == 0 or index == 2:
        rect_bottom = y + height - padding
        rect_left = x + padding
        rect_right = x + width - padding

    elif index == 1:
        rect_bottom = y + height - 35 * padding
        rect_left = x + padding
        rect_right = x + width - padding

    rect_width = rect_right - rect_left
    rect_height = rect_bottom - rect_top
    return rect_left, rect_top, rect_width, rect_height, corner_radius


def get_rounded_rect(scale, rect_width, rect_height, corner_radius):
    # Super sampled rect overlay
    ss_width = rect_width * scale
    ss_height = rect_height * scale
    ss_radius = corner_radius * scale

    ss_image = Image.new("RGBA", (ss_width, ss_height), (0, 0, 0, 0))
    ss_draw = ImageDraw.Draw(ss_image)
    ss_draw.rounded_rectangle(
        [(0, 0), (ss_width, ss_height)],
        radius=ss_radius,
        fill=(0, 0, 0, 100)
    )

    # Step 2: Downscale with anti-aliasing
    rounded_rect = ss_image.resize((rect_width, rect_height), resample=Image.LANCZOS)
    return rounded_rect


def overlay_rect_paste(base_image_size, rounded_rect, rect_left, rect_top):
    # Step 3: Create an overlay and paste the rounded rectangle
    overlay = Image.new("RGBA", base_image_size, (0, 0, 0, 0))
    overlay.paste(rounded_rect, (rect_left, rect_top), mask=rounded_rect)
    return overlay

# def draw_text_on_overlay(overlay, text, font, rect_left, rect_top, rect_width):
#     draw = ImageDraw.Draw(overlay)
#     bbox = font.getbbox(text)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
#     text_x = rect_left + (rect_width - text_width) // 2
#     text_y = rect_top + 10  # inside the box, near the top
#     draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0, 255))