import socket
import bitstring
import io
from select import select
from collections import namedtuple

Bounds = namedtuple("Bounds",["max_contacts", "max_x", "max_y", "max_pressure"])
MinitouchHeader = namedtuple("MinitouchHeader",["version", "bounds", "pid"])

def read_header(sock):
    data = sock.recv(1024)
    lines = data.decode("utf-8").splitlines()
    header = {}
    for line in lines:
        line_arr = line.split(" ")
        field = line_arr[0]
        if field == "v":
            version = int(line_arr[1])
            if(version != 1):
                raise RuntimeError("Unsuppoted minitouch version: {}".format(version))
            header["version"] = version
        elif field == "^":
            header["bounds"] = Bounds(*[int(line_arr[i]) for i in range(1,5)])
        elif field == "$":
            header["pid"] = int(line_arr[1])
    return(MinitouchHeader(**header))

def validate(command):
    # TODO: add command validation
    pass

def send_commands(sock, command_list):
    for command in command_list:
        validate(command)
        sock.sendall(command)

if __name__ == "__main__":
    address = ("",1111)
    with socket.socket() as sock:
        sock.connect(address)
        header = read_header(sock)
        print(header)
