from PIL import Image
from collections import namedtuple
import random
import os

Coords = namedtuple('Coords', 'x y')
Position = namedtuple('Position', 'left right')(0, 1)


def generate_one(bg_file, item_file, output_file, img_size, item_coords):
    back_img = Image.open(bg_file)
    item = Image.open('items/'+item_file)

    back_img.resize((img_size.x, img_size.y))
    item = item.resize((int(img_size.x / 2), int(img_size.y / 2)))

    back_img.paste(item, (item_coords.x, item_coords.y), item)
    back_img.save('outputs/' + output_file, quality=95)


def generate_all_items_fixed_pos(pos, bg_dir, output_dir):
    bgs = os.listdir(bg_dir)
    items = os.listdir('items')
    bgs = [bg for bg in bgs if bg != '.DS_Store']
    items = [item for item in items if item != '.DS_Store']

    for bg in bgs:
        for i in range(0, len(items)):
            img_size = Coords(960, 640)
            print(pos * int(img_size.x/3))
            item_coord = Coords(pos * int(img_size.x/3), 90)
            item_file = str(items[i])

            output_file = output_dir + '/' + str(i) + '.png'
            generate_one(bg_dir + '/' + bg, item_file, output_file, img_size, item_coord)


def generate_all():
    bg_dir = 'background'
    generate_all_items_fixed_pos(Position.left, bg_dir, 'left')
    generate_all_items_fixed_pos(Position.right, bg_dir, 'right')

    generate_all_items_fixed_pos(Position.left, 'outputs/right', 'all')
    generate_all_items_fixed_pos(Position.right, 'outputs/left', 'all')


generate_all()
