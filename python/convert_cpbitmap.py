#!/usr/bin/env python3
"""将 iOS 的 ``cpbitmap`` 文件转换成 PNG 图片。

用法::
    
    python convert_cpbitmap.py <input.cpbitmap> <output.png>
"""
from __future__ import annotations

import math
import struct
import sys
from pathlib import Path

from PIL import Image


def _extract_size(data: bytes) -> tuple[int, int]:
    """Return the (width, height) stored in the cpbitmap footer."""
    if len(data) < 24:
        raise ValueError("File too small to contain footer")
    _, width, height, *_ = struct.unpack("<6i", data[-24:])
    return width, height


def _read_pixels(data: bytes, width: int, height: int) -> bytes:
    """从原始数据中剥离每行末尾的填充字节，返回纯像素数据。"""
    stride = math.ceil(width / 16) * 16 * 4
    row_bytes = width * 4
    pixels = bytearray(row_bytes * height)
    src = 0
    dst = 0
    for _ in range(height):
        pixels[dst : dst + row_bytes] = data[src : src + row_bytes]
        src += stride
        dst += row_bytes
    return bytes(pixels)


def convert(src: Path, dst: Path) -> None:
    """将 ``src`` 转换为 PNG 并保存到 ``dst``。"""
    data = src.read_bytes()
    width, height = _extract_size(data)
    pixel_data = _read_pixels(data, width, height)

    img = Image.frombuffer("RGBA", (width, height), pixel_data, "raw", "BGRA")
    img.save(dst)


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="cpbitmap \u8f6c\u6362\u5de5\u5177")
    parser.add_argument("src", type=Path, help="\u8f93\u5165 cpbitmap \u6587\u4ef6")
    parser.add_argument("dst", type=Path, help="\u8f93\u51fa PNG \u6587\u4ef6")
    args = parser.parse_args(argv)

    convert(args.src, args.dst)
    print(f"Saved {args.dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
