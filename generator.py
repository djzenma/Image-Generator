from PIL import Image
from collections import namedtuple
import os

# Struct
Coords = namedtuple('Coords', 'x y')
# Enum
Position = namedtuple('Position', 'left right')(0, 1)


# Paste a the item specified on the bg specified
def generate_one(bg_file, item_file, output_file, img_size, item_coords):
    # Open the 2 images
    back_img = Image.open(bg_file)
    item = Image.open('items/'+item_file)

    # Resize Them
    back_img.resize((img_size.x, img_size.y))
    item = item.resize((int(img_size.x / 2), int(img_size.y / 2)))

    # Paste the item on the bg
    back_img.paste(item, (item_coords.x, item_coords.y), item)

    # Save the result
    back_img.save('outputs/' + output_file, quality=95)


# Paste all the items specified on all the bgs specified
def generate_all_items_fixed_pos(pos, bg_dir, output_dir):
    # Get the list of the Backgrounds and the Items
    bgs = os.listdir(bg_dir)
    items = os.listdir('items')
    bgs = [bg for bg in bgs if bg != '.DS_Store']
    items = [item for item in items if item != '.DS_Store']

    # Paste every item in every background on the position specified in the parameter
    for bg in bgs:  # For every background
        for i in range(0, len(items)):  # Paste every item
            # Specify output size & item size
            img_size = Coords(960, 640)
            item_coord = Coords(pos * int(img_size.x/3), 90)
            item_file = str(items[i])

            # output directory
            output_file = output_dir + '/' + str(i) + '.png'
            generate_one(bg_dir + '/' + bg, item_file, output_file, img_size, item_coord)


# Generate all items both on the left and on the right of every bg
def generate_all():
    bg_dir = 'background'
    # Paste all items on the left of every bg
    generate_all_items_fixed_pos(Position.left, bg_dir, 'left')
    # Paste all items on the right of every bg
    generate_all_items_fixed_pos(Position.right, bg_dir, 'right')

    # Paste all items on the left of every bg with item on its right
    generate_all_items_fixed_pos(Position.left, 'outputs/right', 'all')
    # Paste all items on the right of every bg with item on its left
    generate_all_items_fixed_pos(Position.right, 'outputs/left', 'all')


generate_all()
