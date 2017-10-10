import itertools
from ..datatypes import Box, ContentBox

def _is_parent(box1, box2):
    return ((box1.x <= box2.x)
            and (box1.y <= box2.y)
            and (box1.x+box1.w >= box2.x+box2.w)
            and (box1.y+box1.h >= box2.y+box2.h))

def filter_parent_boxes(areas):
    areas_copy = list(areas)
    for box1,box2 in itertools.permutations(areas_copy, 2):
        if (_is_parent(box1,box2) and (box1 in areas_copy)):
            areas_copy.remove(box1)
    return areas_copy

def add_box_paddings(box_arr, max_width, max_height, paddings_arr=[5,5,10,10]):
    x,y,w,h = box_arr
    dx,dy,dw,dh = paddings_arr
    x -= min([dx, x])
    y -= min([dy, y])
    w += min([dw, max_width-w])
    h += min([dh, max_height-w])
    return Box(x,y,w,h)

def rebase_box(boxes, dx, dy, c_w, c_h, o_w, o_h):
    # c_w, c_h - croped   width and height
    # o_w, o_h - original width and height
    x = (box.position.x * c_w / o_w + dx for box in boxes)
    y = (box.position.y * c_h / o_h + dy for box in boxes)
    w = (box.position.w * c_w / o_w for box in boxes)
    h = (box.position.h * c_h / o_h for box in boxes)
    positions = (Box(*pos) for pos in zip(x,y,w,h))
    return [ContentBox(box.content, position) for box, position in zip (boxes, positions)]

def abs_to_rel(boxes, width, height):
    positions = (box.position for box in boxes)
    rel_positions = (Box(pos.x / width, pos.y / height, pos.w / width, pos.h / height) for pos in positions)
    return [ContentBox(box.content, rel_pos) for box,rel_pos in zip(boxes, rel_positions)]
