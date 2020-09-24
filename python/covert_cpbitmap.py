from PIL import Image
import sys
import math
import struct
import os


def func2():
    def r8(f):
        c = ord(f.read(1))
        return c

    if len(sys.argv) <= 2:
        print("Usage: %s <input> <output>" % sys.argv[0])
    else:
        source = os.path.abspath(sys.argv[1])

        f = open(source, "rb")
        f.seek(-78, 2)
        magic = f.read(8)
        print(magic)
        # if magic != r"bplist00":
        #     print("Didn't find bplist header, are you sure this is a cpbitmap file?")
        #     exit(1)
        f.seek(50, 1)
        dat = f.read(6)
        width, height = struct.unpack("<HxxH", dat)
        print("Size: %dx%d" % (width, height))
        img = Image.new("RGBA", (width, height))

        f.seek(0)
        imgd = img.load()

        # Take care of the line size
        line_size = int(math.ceil(width/16.0) * 16)
        print(line_size)
        for y in range(height):
            for x in range(width):
                b, g, r, a = r8(f), r8(f), r8(f), r8(f)
                imgd[x, y] = (r, g, b, a)
            f.seek((line_size - width)*4, 1)

        f.close()
        img.save(sys.argv[2])


if __name__ == "__main__":
    func2()
