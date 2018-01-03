#!/usr/bin/python
# by @wenxingxing
# usage python unwxapkg.py filename

import sys, os
import struct


class WxapkgFile:
    nameLen = 0
    name = ""
    offset = 0
    size = 0


if len(sys.argv) < 2:
    print('usage: unwxapkg.py filename')
    exit()

with open(sys.argv[1], "rb") as f:

    root = os.path.dirname(os.path.realpath(f.name))
    name = os.path.basename(f.name)

    if len(sys.argv) > 2:
        name = sys.argv[2]

    #read header

    firstMark = struct.unpack('B', f.read(1))[0]
    print('first header mark = ' + str(firstMark))

    info1 = struct.unpack('>L', f.read(4))[0]
    print('info1 = ' + str(info1))

    indexInfoLength = struct.unpack('>L', f.read(4))[0]
    print('indexInfoLength = ' + str(indexInfoLength))

    bodyInfoLength = struct.unpack('>L', f.read(4))[0]
    print('bodyInfoLength = ' + str(bodyInfoLength))

    lastMark = struct.unpack('B', f.read(1))[0]
    print('last header mark = ' + str(lastMark))

    if firstMark != 0xBE or lastMark != 0xED:
        print('its not a wxapkg file!!!!!')
        exit()

    fileCount = struct.unpack('>L', f.read(4))[0]
    print('fileCount = ' + str(fileCount))

    #read index

    fileList = []

    for i in range(fileCount):

        data = WxapkgFile()
        data.nameLen = struct.unpack('>L', f.read(4))[0]
        data.name = f.read(data.nameLen)
        data.offset = struct.unpack('>L', f.read(4))[0]
        data.size = struct.unpack('>L', f.read(4))[0]

        print('readFile = ' + data.name + ' at Offset = ' + str(data.offset))

        fileList.append(data)

    #save files

    for d in fileList:
        path = root + '/' + name + '_'
        file_ = path + d.name

        if not os.path.exists(os.path.dirname(file_)):
            os.makedirs(os.path.dirname(file_))

        w = open(file_, 'w')
        f.seek(d.offset)
        w.write(f.read(d.size))
        w.close()

        print('writeFile = ' + file_)

    f.close()