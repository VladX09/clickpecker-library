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

def touch(point, time=0):
    return _concat([down(*point),
                   commit(),
                   up(point[0]),
                   commit(),
                   wait(time),
                   commit()])
