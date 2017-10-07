import itertools
from ..datatypes import Box

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
    return [x,y,w,h]
