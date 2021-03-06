from functools import reduce, partial
from math import floor

_concat = partial(reduce, (lambda x, y: x + y))


def commit():
    return ["c"]


def down(contact, x, y, pressure):
    x, y = floor(x), floor(y)
    pressure = floor(pressure)
    return ["d {} {} {} {}".format(contact, x, y, pressure)]


def up(contact):
    return ["u {}".format(contact)]


def move(contact, new_x, new_y, pressure):
    new_x, new_y = floor(new_x), floor(new_y)
    pressure = floor(pressure)
    return ["m {} {} {} {}".format(contact, new_x, new_y, pressure)]


def wait(time):
    return ["w {}".format(time)]


def touch(contact, x, y, pressure, time=0):
    x, y = floor(x), floor(y)
    pressure = floor(pressure)
    return _concat([
        down(contact, x, y, pressure),
        commit(),
        wait(time),
        up(contact),
        commit(),
        commit()
    ])


def drag(contact, x1, y1, x2, y2, pressure, step):
    x1, y1 = floor(x1), floor(y1)
    x2, y2 = floor(x2), floor(y2)
    pressure = 1 if pressure <= 0 else floor(pressure)
    start_point = (contact, x1, y1, pressure)
    mov = [down(*start_point), commit()]
    for i in range(0, 100, step):
        x = x1 + ((x2 - x1) // 100 * i)
        y = y1 + ((y2 - y1) // 100 * i)
        new_point = (contact, x, y, pressure)
        mov.append(move(*new_point))
        mov.append(commit())
        mov.append(wait(1))
        mov.append(commit())
    last_point = (contact, x2, y2, pressure)
    mov.append(move(*last_point))
    mov.append(commit())
    mov.append(up(contact))
    mov.append(commit())
    return _concat(mov)


def scroll(minitouch_bounds, from_point_rel, to_point_rel):
    _, max_x, max_y, max_pressure = minitouch_bounds
    max_point = [max_x, max_y]
    from_point_abs = [i * j for i, j in zip(from_point_rel, max_point)]
    to_point_abs = [i * j for i, j in zip(to_point_rel, max_point)]
    return drag(0, *from_point_abs, *to_point_abs, max_pressure, 30)
