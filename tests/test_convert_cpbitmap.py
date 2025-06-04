import math
import struct
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'python'))

import convert_cpbitmap as cp

SAMPLE = Path(__file__).resolve().parents[1] / 'samples' / 'LockBackground.cpbitmap'

def test_extract_size_sample():
    data = SAMPLE.read_bytes()
    width, height = cp._extract_size(data)
    assert (width, height) == (1943, 2591)

def test_read_pixels_length():
    data = SAMPLE.read_bytes()
    width, height = cp._extract_size(data)
    pixels = cp._read_pixels(data, width, height)
    assert len(pixels) == width * height * 4
    assert pixels[:16] == data[:16]

def test_extract_size_small_file_error():
    try:
        cp._extract_size(b'123')
    except ValueError:
        pass
    else:
        raise AssertionError('ValueError not raised')

def test_read_pixels_padding():
    width, height = 5, 2
    stride = math.ceil(width / 16) * 16 * 4
    buf = bytearray(stride * height)
    for y in range(height):
        for x in range(stride // 4):
            start = y * stride + x * 4
            buf[start:start+4] = struct.pack('BBBB', x, x, x, 255)
    footer = struct.pack('<6i', 0, width, height, 0, 0, 0)
    data = bytes(buf) + footer
    pixels = cp._read_pixels(data, width, height)
    expected = b''.join(
        struct.pack('BBBB', x, x, x, 255)
        for y in range(height)
        for x in range(width)
    )
    assert pixels == expected
