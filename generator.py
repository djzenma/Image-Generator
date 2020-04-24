from PIL import Image
from collections import namedtuple
import os
import shutil

# Struct
Coords = namedtuple('Coords', 'x y')
# Enum
Position = namedtuple('Position', 'left right')(0, 1)
counter = 0


# Paste a the item specified on the bg specified
def generate_one(bg_file, item_file, output_file, img_size, item_coords):
    # Open the 2 images
    back_img = Image.open(bg_file)
    item = Image.open(item_file)
    category = item_file.split('/')[1]
    # TODO::To be removed
    if category == 'Man' or category == 'Woman' or category == 'Girl' or category == 'Boy':
        div = 0.8
    else:
        div = 1.5
    # Resize Them
    back_img.resize((img_size.x, img_size.y))
    item = item.resize((int(img_size.x / 2), int(img_size.y / div)))

    # Paste the item on the bg
    back_img.paste(item, (item_coords.x, item_coords.y), item)

    # Save the result
    back_img.save('outputs/' + output_file, quality=95)


# Paste all the items specified on all the bgs specified
def generate_all_items_fixed_pos(pos, bg_dir, items_dir, output_dir):
    # Get the list of the Backgrounds and the Items
    bgs = os.listdir(bg_dir)
    items = os.listdir(items_dir)
    bgs = [bg for bg in bgs if bg != '.DS_Store']
    items = [item for item in items if item != '.DS_Store']
    category = items_dir.replace('items/', '')
    global counter
    # Paste every item in every background on the position specified in the parameter
    for bg in bgs:  # For every background
        for i in range(0, len(items)):  # Paste every item
            # TODO:: To be removed
            if category == 'Man' or category == 'Woman' or category == 'Girl' or category == 'Boy':
                div = 2.2
                height = 150
            else:
                div = 2.5
                height = 210
            # Specify output size & item size
            img_size = Coords(960, 640)
            item_coord = Coords(pos * int(img_size.x/div), height)
            item_file = items_dir + '/' + str(items[i])

            # output directory
            output_file = output_dir + '/' + str(counter) + '.png'
            counter += 1
            generate_one(bg_dir + '/' + bg, item_file, output_file, img_size, item_coord)


# Generate all items both on the left and on the right of every bg
def generate_all():
    if os.path.exists('outputs/left_tmp'):
        shutil.rmtree('outputs/left_tmp')
    if os.path.exists('outputs/right_tmp'):
        shutil.rmtree('outputs/right_tmp')

    bg_dir = 'background'
    items_categories = os.listdir('items')
    items_categories = [cat for cat in items_categories if cat != '.DS_Store']
    for item_cat in items_categories:
        #os.mkdir('outputs/left_tmp')
        #os.mkdir('outputs/right_tmp')
        items_dir = 'items' + '/' + item_cat
        # Paste all items on the left of every bg
        generate_all_items_fixed_pos(Position.left, bg_dir, items_dir, 'left')
        #generate_all_items_fixed_pos(Position.left, bg_dir, items_dir, 'left_tmp')
        # Paste all items on the right of every bg
        generate_all_items_fixed_pos(Position.right, bg_dir, items_dir, 'right')
        #generate_all_items_fixed_pos(Position.right, bg_dir, items_dir, 'right_tmp')

    for item_cat in items_categories:
        items_dir = 'items' + '/' + item_cat
        # Paste all items on the left of every bg with item on its right
        generate_all_items_fixed_pos(Position.left, 'outputs/right', items_dir, 'all')
        # Paste all items on the right of every bg with item on its left
        generate_all_items_fixed_pos(Position.right, 'outputs/left', items_dir, 'all')
        #shutil.rmtree('outputs/left_tmp')
        #shutil.rmtree('outputs/right_tmp')
        print("Finished category: " + str(item_cat))


print("working...")
generate_all()
print("done")
