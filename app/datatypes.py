from collections import namedtuple

ContentBox = namedtuple("ContentBox", ["content", "position"])
Box = namedtuple("Box", ["x","y","w","h"])
MinitouchBounds = namedtuple("MinitouchBounds",["max_contacts", "max_x", "max_y", "max_pressure"])
MinitouchHeader = namedtuple("MinitouchHeader",["version", "bounds", "pid"])
MinicapKeys = ["version",
               "header_size",
               "pid",
               "real_width",
               "real_height",
               "virtual_width",
               "virtual_height",
               "orientation",
               "quirk"]
MinicapHeader = namedtuple("MinicapHeader", MinicapKeys)
