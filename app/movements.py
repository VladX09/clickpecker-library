from functools import reduce, partial

_concat = partial(reduce, (lambda x,y: x + y))

def commit():
    return ["c"]

def down(contact, x, y, pressure):
    return ["d {} {} {} {}".format(contact, x, y, pressure)]

def up(contact):
    return ["u {}".format(contact)]

def move(contact, new_x, new_y, pressure):
    return ["m {} {} {} {}".format(contact, new_x, new_y, pressure)]

def wait(time):
    return ["w {}".format(time)]

def touch(contact, x, y, pressure, time=0):
    return _concat([down(contact, x, y, pressure),
                   commit(),
                   wait(time),
                   up(contact),
                   commit(),
                   commit()
    ])

def drag(contact, x1, y1, x2, y2, pressure, step):
    start_point = (contact, x1, y1, pressure)
    mov = [down(*start_point), commit()]
    for i in range(0, 1, step):
        x = x1 + ((x2 - x1) * i)
        y = y1 + ((y2 - y1) * i)
        new_point = (contact, x, y, pressure)
        mov.append(move(*new_point))
        mov.append(commit())
    mov.append(up(contact))
    mov.append(commit())
    return _concat(mov)
