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

def basic_postprocessing(content_boxes, zoom=0.5):
    new_boxes = []
    for box in content_boxes:
        new_content = replace_ligatures(box.content).lower().replace(" ","").strip().replace("\n","")
        new_position = Box(*[dim * zoom for dim in box.position])
        new_boxes.append(ContentBox(new_content, new_position))
    return new_boxes
