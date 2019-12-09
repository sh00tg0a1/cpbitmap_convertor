#!/usr/bin/python2
from PIL import Image,ImageOps
import struct
import sys

def func1():
    if len(sys.argv) < 3:
        print "Need two args: filename and result_filename\n"
        sys.exit(0)
    filename = sys.argv[1]
    result_filename = sys.argv[2]

    with open(filename) as f:
        contents = f.read()
        print len(contents)
        unk1, width, height, unk2, unk3, unk4 = struct.unpack('<6i', contents[-24:])
        print unk1, width, height, unk2, unk3, unk4
        im = Image.frombytes('RGBA', (width, height), contents, 'raw', 'RGBA', 0, 1)
        r,g,b,a = im.split()
        im = Image.merge('RGBA', (b,g,r,a))
        im.save(result_filename)


def func2():
    from PIL import Image
    import sys
    import math
    import struct

    def r8(f):
        c = ord(f.read(1))
        return c

    if len(sys.argv) <= 2:
        print("Usage: %s <input> <output>" % sys.argv[0])
    else:
        f = open(sys.argv[1], "rb")
        f.seek(-78, 2)
        magic = f.read(8)
        print magic
        if magic != "bplist00":
            print("Didn't find bplist header, are you sure this is a cpbitmap file?")
            exit(1)
        f.seek(50, 1)
        dat = f.read(6)
        width, height = struct.unpack("<HxxH", dat)
        print("Size: %dx%d" % (width, height))
        img = Image.new("RGBA", (width, height))

        f.seek(0)
        imgd = img.load()

        # Take care of the line size
        line_size = int(math.ceil(width/16.0) * 16)
        print line_size
        for y in range(height):
            for x in range(width):
                b, g, r, a = r8(f), r8(f), r8(f), r8(f)
                imgd[x, y] = (r, g, b, a)
            f.seek((line_size - width)*4, 1)

        f.close()
        img.save(sys.argv[2])

func2()
