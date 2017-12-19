import socket
import bitstring
import io
import re
import time

from select import select
from collections import namedtuple

MinitouchBounds = namedtuple(
    "MinitouchBounds", ["max_contacts", "max_x", "max_y", "max_pressure"])

MinitouchHeader = namedtuple("MinitouchHeader", ["version", "bounds", "pid"])


def read_header(sock):
    data = sock.recv(1024)
    lines = data.decode("utf-8").splitlines()
    header = {}
    for line in lines:
        line_arr = line.split(" ")
        field = line_arr[0]
        if field == "v":
            version = int(line_arr[1])
            if (version != 1):
                raise RuntimeError(
                    "Unsuppoted minitouch version: {}".format(version))
            header["version"] = version
        elif field == "^":
            header["bounds"] = MinitouchBounds(
                * [int(line_arr[i]) for i in range(1, 5)])
        elif field == "$":
            header["pid"] = int(line_arr[1])
    return (MinitouchHeader(**header))


def validate(command):
    pattern = r"[crdmuw]( [\d]*){0,4}"
    if re.fullmatch(pattern, command) == None:
        raise RuntimeError("Wrong minitouch command: {}".format(command))


def send_commands(sock, command_list):
    sock.recv(1024)
    for command in command_list:
        validate(command)
        if command[0] == "w":
            sleep_time = int(command.split(" ")[1])
            time.sleep(sleep_time)
        else:
            sock.sendall((command + "\n").encode("utf-8"))
