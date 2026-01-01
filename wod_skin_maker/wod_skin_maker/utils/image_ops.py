# utils/image_ops.py - Image processing utilities

from PIL import Image, ImageDraw, ImageOps

def apply_broken_effect(full_image, broken_ref):
    """Apply broken dot mask to full health image"""
    br_resized = broken_ref.resize(full_image.size, Image.Resampling.LANCZOS)
    mask = br_resized.split()[3]  # alpha channel
    result = full_image.copy()
    result.putalpha(mask)
    return result

def create_circle_mask(width, height, center_x, center_y, radius):
    """Create a circular mask"""
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    x1 = center_x - radius
    y1 = center_y - radius
    x2 = center_x + radius
    y2 = center_y + radius
    draw.ellipse((x1, y1, x2, y2), fill=255)
    return mask

def apply_circle_crop(image, center_x, center_y, radius):
    """Crop image to circle"""
    w, h = image.size
    mask = create_circle_mask(w, h, center_x, center_y, radius)
    cropped = Image.new("RGBA", (w, h))
    cropped.paste(image, (0, 0), mask)
    return cropped

def flip_image(image, direction):
    """Flip image horizontally or vertically"""
    if direction == "horizontal":
        return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return image

def rotate_image(image, degrees):
    """Rotate image by specified degrees"""
    return image.rotate(degrees, expand=False)

def resize_to_64(image):
    """Resize image to 64x64"""
    return image.resize((64, 64), Image.Resampling.LANCZOS)
