#!/usr/bin/env python3
"""Minimal SZDD (Microsoft COMPRESS.EXE 'A' variant) decompressor."""
import sys

MAGIC = bytes([0x53, 0x5A, 0x44, 0x44, 0x88, 0xF0, 0x27, 0x33])

def expand(data: bytes) -> bytes:
    assert data[:8] == MAGIC, "not an SZDD/'A' stream"
    assert data[8:9] == b'A', "unexpected compression mode"
    out_len = int.from_bytes(data[10:14], "little")
    win = bytearray([0x20] * 4096)
    pos = 4096 - 16
    out = bytearray()
    i = 14
    n = len(data)
    while i < n and len(out) < out_len:
        ctrl = data[i]; i += 1
        for bit in range(8):
            if i >= n or len(out) >= out_len:
                break
            if ctrl & (1 << bit):                       # literal
                b = data[i]; i += 1
                out.append(b); win[pos] = b; pos = (pos + 1) & 0xFFF
            else:                                       # back-reference
                if i + 1 >= n:
                    i = n; break
                lo = data[i]; hi = data[i + 1]; i += 2
                mpos = lo | ((hi & 0xF0) << 4)
                mlen = (hi & 0x0F) + 3
                for _ in range(mlen):
                    b = win[mpos & 0xFFF]; mpos += 1
                    out.append(b); win[pos] = b; pos = (pos + 1) & 0xFFF
                    if len(out) >= out_len:
                        break
    return bytes(out[:out_len])

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        raw = f.read()
    res = expand(raw)
    with open(sys.argv[2], "wb") as f:
        f.write(res)
    print(f"in={len(raw)}  out={len(res)}  header={res[:2]!r}")
