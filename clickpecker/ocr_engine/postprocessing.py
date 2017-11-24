from ..datatypes import Box, ContentBox


def _get_ligature_replaces():
    ligatures = {
        "\N{latin capital ligature oe}": "OE",
        "\N{latin capital ligature ij}": "IJ",
        "\N{latin small ligature oe}": "oe",
        "\N{latin small ligature ij}": "ij",
        "\N{latin small ligature ff}": "ff",
        "\N{latin small ligature fi}": "fi",
        "\N{latin small ligature fl}": "fl",
        "\N{latin small ligature ffi}": "ffi",
        "\N{latin small ligature ffl}": "ffl",
        "\N{latin small ligature st}": "st",
        "\N{modifier letter small ligature oe}": "oe"
    }
    return ligatures


def replace_ligatures(str):
    for ligature, replacement in _get_ligature_replaces().items():
        str = str.replace(ligature, replacement)
    return str


def compose_in_lines(content_boxes, threshold=0.6):
    def compose_line(line):
        line = sorted(line, key=lambda box: box.position.x)
        start_x = line[0].position.x
        start_y = line[0].position.y
        end_x = line[-1].position.x + line[-1].position.w
        end_y = line[-1].position.y + line[-1].position.h
        line_box = Box(start_x, start_y, end_x - start_x, end_y - start_y)
        line_content = "".join(["{} ".format(box.content)
                                for box in line]).strip()
        return ContentBox(line_content, line_box)

    lines = []
    line = []
    for box in sorted(content_boxes, key=lambda box: box.position.y):
        if not line:
            y_up = box.position.y
            y_down = y_up + box.position.h
            line.append(box)
            continue
        y = box.position.y
        h = box.position.h
        if (min([y_down, y + h]) - max([y_up, y]) >= threshold * h):
            line.append(box)
        else:
            lines.append(compose_line(line))
            line = [box]
            y_up = box.position.y
            y_down = y_up + box.position.h

    if line:
        lines.append(compose_line(line))
        line = []
    return lines


def basic_postprocessing(content_boxes):
    new_content = (replace_ligatures(box.content).lower().replace(" ", "")
                   .strip().replace("\n", "") for box in content_boxes)
    new_position = (box.position for box in content_boxes)
    return compose_in_lines(
        [ContentBox(*b) for b in zip(new_content, new_position)])
