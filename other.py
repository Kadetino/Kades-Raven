from PIL import Image


def web_pfp_gen(img1: str, img2: str):
    # Open the two input images
    image1 = Image.open(f'images/{img1}.png').convert("RGBA")
    image2 = Image.open(f'images/{img2}.png').convert("RGBA")
    # Verify
    if image1.size != (24, 24) or image2.size != (24, 24):
        raise ValueError("Both images should be 24x24 pixels.")
    # Create blank
    new_image = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    # Paste
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (0, 0), image2)

    return
