#!/usr/bin/env python3
# encoding: utf-8
import socket


def connect():
    # _s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    _s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    _s.connect('/tmp/test.sock')
    return _s


def send(_s, msg):
    from struct import pack, calcsize
    import sys
    file = _s.makefile('wb')
    # size_of_data = sys.getsizeof(msg)
    # print("len: ", size_of_data)
    # limit = 2048 - calcsize('I')
    # remainder = size_of_data % limit
    # print("re: ", remainder)
    # loop = int((size_of_data - remainder) / limit)
    # print("loop", loop)
    # start = 0
    # while start < loop:
    #     _now = start + 1
    #     print("%s: " % _now)
    #     print("From: %s to %s" % (start*limit, _now*limit))
    #     _data_to_send = msg[start*limit:_now*limit]
    #     file.write(pack("I%ds" % (len(_data_to_send),), len(_data_to_send), _data_to_send.encode()))
    #     file.flush()
    #     start += 1
    # if remainder > 0:
    #     print("From: %s to %s" % (limit*loop, size_of_data))
    #     _data_to_send = msg[limit*loop:size_of_data]
    #     file.write(pack("I%ds" % (len(_data_to_send),), len(_data_to_send), _data_to_send.encode()))
    #     file.flush()
    # _s2 = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    print("size of data: %s" % sys.getsizeof(msg))
    packed_data = pack("I%ds" % (len(msg),), len(msg), msg.encode())
    file.write(packed_data)
    file.flush()
    # _s2.sendto(packed_data, '/tmp/test.sock')


def as_file(_s):
    return _s.makefile('w')


if __name__ == "__main__":
    ddd = '''Starting phase 4/4: Write Checkpoint tables into "/cache/level1-3/plot-k32-2021-05-12-17-12-0aeb47588db6905b773e05c79ad785a00733132eecf81e376eb908307f387280.plot.2.tmp" ... Thu May 13 00:21:26 2021
        Starting to write C1 and C3 tables
        Bucket 0 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 1 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 2 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 3 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 4 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 5 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 6 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 7 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 8 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 9 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 10 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 11 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 12 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 13 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 14 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 15 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 16 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 17 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 18 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 19 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 20 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 21 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 22 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 23 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 24 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 25 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 26 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 27 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 28 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 29 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 30 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 31 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 32 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 33 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 34 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 35 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 36 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 37 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 38 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 39 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 40 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 41 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 42 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 43 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 44 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 45 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 46 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 47 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 48 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 49 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 50 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 51 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 52 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 53 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 54 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 55 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs min: 0.281GiB.
        Bucket 56 uniform sort. Ram: 3.352GiB, u_sort min: 0.563GiB, qs min: 0.281GiB.
        Bucket 57 uniform sort. Ram: 3.352GiB, u_sort min: 1.125GiB, qs mi''' * 3
    s = connect()
    send(s, ddd)
    send(s, ddd)
