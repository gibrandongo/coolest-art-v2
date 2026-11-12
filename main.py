#!/usr/bin/env python3
"""coolest-art-01 entry: copy the bundled artwork to /output/entry.png.

The artwork is a JPEG stored beside this program as entry.jpg. The
competition contract names the output file entry.png either way and tells
PNG from JPEG by the file's first bytes, so the JPEG bytes are copied
verbatim — no re-encoding, no transformation. The copy is deterministic:
the same input bytes always produce the same output bytes.
"""

import os
import sys

SOURCE_NAME = "entry.jpg"
OUTPUT_NAME = "entry.png"
MAX_BYTES = 1048576

# JPEG start-of-image and end-of-image markers. The gate requires a whole
# image, so refuse to ship bytes that are not a complete JPEG.
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


def check_payload(payload):
    """Reject anything that is not a whole JPEG inside the size cap."""
    if len(payload) > MAX_BYTES:
        raise ValueError("artwork is %d bytes, over the 1 MiB cap" % len(payload))
    if not payload.startswith(JPEG_SOI):
        raise ValueError("artwork does not start with the JPEG SOI marker")
    if not payload.rstrip().endswith(JPEG_EOI):
        raise ValueError("artwork does not end with the JPEG EOI marker")


def output_directory():
    """Where the grader wants the artifact.

    Local runs set MAKEFUN_OUTPUT_DIR; the grading sandbox mounts the
    writable directory at /output.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    with open(source, "rb") as handle:
        payload = handle.read()
    check_payload(payload)
    out_dir = output_directory()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    # Write to a temp file in the same directory, then rename, so the
    # artifact appears whole or not at all — never half-written.
    staging = target + ".tmp"
    with open(staging, "wb") as handle:
        handle.write(payload)
    os.replace(staging, target)
    print("wrote %s: %d bytes" % (target, len(payload)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
