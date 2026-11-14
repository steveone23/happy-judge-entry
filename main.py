"""Entry for the make.fun bounty "Make the AI judge happy" (ai-happy-01).

Copies the committed image at assets/entry.png, byte for byte, to
/output/entry.png. Before writing, it checks that the file is a PNG or JPEG
(by signature, not by name), at most 1 MiB and at most 1024 by 1024 pixels.
The output is fully deterministic: every run writes the same bytes.
Standard library only, no network access.
"""

import hashlib
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "assets" / "entry.png"
TARGET = Path("/output/entry.png")
MAX_BYTES = 1024 * 1024  # 1 MiB
MAX_SIDE = 1024  # pixels
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"
# SOF0 to SOF15, except DHT (0xC4), JPG (0xC8) and DAC (0xCC).
JPEG_SOF_MARKERS = set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}


def png_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) from the IHDR chunk, which must come first."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    return struct.unpack(">II", data[16:24])


def jpeg_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) by walking the markers to the first SOF header."""
    pos = 2  # skip SOI
    while pos < len(data):
        if data[pos] != 0xFF:
            raise ValueError(f"JPEG marker expected at offset {pos}")
        while pos < len(data) and data[pos] == 0xFF:  # skip fill bytes
            pos += 1
        if pos >= len(data):
            break
        marker = data[pos]
        pos += 1
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:  # TEM, RSTn: no length
            continue
        if marker in (0xD9, 0xDA):  # EOI or SOS before any frame header
            break
        if pos + 2 > len(data):
            break
        (length,) = struct.unpack(">H", data[pos:pos + 2])
        if length < 2:
            raise ValueError(f"bad JPEG segment length at offset {pos}")
        if marker in JPEG_SOF_MARKERS:
            if pos + 7 > len(data):
                break
            height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
            return width, height
        pos += length
    raise ValueError("JPEG has no frame header")


def main() -> int:
    data = SOURCE.read_bytes()
    if data.startswith(PNG_SIGNATURE):
        kind, (width, height) = "PNG", png_size(data)
    elif data.startswith(JPEG_SIGNATURE):
        kind, (width, height) = "JPEG", jpeg_size(data)
    else:
        sys.exit(f"error: {SOURCE} is not a PNG or JPEG file")
    if len(data) > MAX_BYTES:
        sys.exit(f"error: {SOURCE} is {len(data)} bytes, limit is {MAX_BYTES}")
    if not (0 < width <= MAX_SIDE and 0 < height <= MAX_SIDE):
        sys.exit(f"error: {SOURCE} is {width}x{height}, limit is {MAX_SIDE}x{MAX_SIDE}")

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {TARGET}: {kind} {width}x{height}, {len(data)} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
