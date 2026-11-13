"""Copy picture.jpg to entry.png; the JPEG bytes use the required entry filename."""

import os
import sys
from pathlib import Path


def main() -> int:
    source = Path(__file__).resolve().parent / "picture.jpg"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")).resolve()
    destination = output_dir / "entry.png"

    try:
        data = source.read_bytes()
    except OSError as error:
        print(f"Unable to read source image {source}: {error}", file=sys.stderr)
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        written_size = destination.stat().st_size
    except OSError as error:
        print(f"Unable to write output image {destination}: {error}", file=sys.stderr)
        return 1

    if written_size != len(data):
        print(
            f"Output size check failed for {destination}: expected {len(data)} bytes, "
            f"found {written_size} bytes",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {destination}: {written_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
