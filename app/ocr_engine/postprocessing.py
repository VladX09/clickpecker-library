from ..namedtuples import Box, ContentBox

def _get_ligature_replaces():
    ligatures = {"\N{latin capital ligature oe}":"OE",
                 "\N{latin capital ligature ij}":"IJ",
                 "\N{latin small ligature oe}":"oe",
                 "\N{latin small ligature ij}":"ij",
                 "\N{latin small ligature ff}":"ff",
                 "\N{latin small ligature fi}":"fi",
                 "\N{latin small ligature fl}":"fl",
                 "\N{latin small ligature ffi}":"ffi",
                 "\N{latin small ligature ffl}":"ffl",
                 "\N{latin small ligature st}":"st",
                 "\N{modifier letter small ligature oe}":"oe"}
    return ligatures

def replace_ligatures(str):
    for ligature, replacement in _get_ligature_replaces().items():
        str = str.replace(ligature, replacement)
    return str

def compose_strings(content_boxes, threshold=0.6):
    lines = []
    new_line = True
    for box in sorted(content_boxes, key=lambda box: box.position.y):
        if new_line:
            # TODO: add appending if newline is last box 
            y_up = box.position.y
            y_down =y_up + box.position.h
            line_content = box.content
            start_pos = box.position
            end_pos = box.position
            new_line = False
            print("Up:{0} \nDown:{1}".format(y_up, y_down))
            print("Start: ({pos.x},{pos.y},{pos.w},{pos.h})".format(pos = start_pos))
            print("End: ({pos.x},{pos.y},{pos.w},{pos.h})".format(pos = end_pos))
            print("Content:{0}".format(line_content))
            print(" ")
            continue
        y = box.position.y
        h = box.position.h
        print("Box: ({0},{1})".format(y,y+h))
        if (min([y_down, y + h]) - max([y_up, y]) >= threshold * h):
            # TODO: add line content arranging according to x coordinate
            line_content += " " + box.content
            start_pos = min([start_pos, box.position], key=lambda p:p.x)
            end_pos = max([end_pos, box.position], key=lambda p:p.x)
        else:
            new_line = True
            line_end_x = end_pos.x + end_pos.w
            line_end_y = end_pos.y + end_pos.h
            line_position = Box(start_pos.x, start_pos.y, line_end_x - start_pos.x, line_end_y - start_pos.y)
            lines.append(ContentBox(line_content, line_position))
        print("Start: ({pos.x},{pos.y},{pos.w},{pos.h})".format(pos = start_pos))
        print("End: ({pos.x},{pos.y},{pos.w},{pos.h})".format(pos = end_pos))
        print("Content:{0}".format(line_content))
        print(" ")
    return lines

def basic_postprocessing(content_boxes, zoom=0.5):
    new_boxes = []
    for box in content_boxes:
        new_content = replace_ligatures(box.content).lower().replace(" ","").strip().replace("\n","")
        new_position = Box(*[dim * zoom for dim in box.position])
        new_boxes.append(ContentBox(new_content, new_position))
    return compose_strings(new_boxes)
