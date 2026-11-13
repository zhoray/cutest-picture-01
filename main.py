"""Copy the entry's JPEG image to entry.png, the filename required by the competition."""

import hashlib
import os
import sys
import tempfile
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    source = Path(__file__).resolve().parent / "picture.jpg"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    temporary_path: Path | None = None

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with source.open("rb") as image:
            source_digest = hashlib.sha256()
            byte_count = 0
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=output_dir, prefix=".entry.png.", suffix=".tmp", delete=False
            ) as output:
                temporary_path = Path(output.name)
                for chunk in iter(lambda: image.read(1024 * 1024), b""):
                    output.write(chunk)
                    source_digest.update(chunk)
                    byte_count += len(chunk)

        os.replace(temporary_path, output_dir / "entry.png")
        temporary_path = None

        source_hash = source_digest.hexdigest()
        output_hash = sha256_file(output_dir / "entry.png")
        if output_hash != source_hash:
            print(
                f"Integrity check failed: entry.png SHA-256 {output_hash} does not match "
                f"picture.jpg SHA-256 {source_hash}",
                file=sys.stderr,
            )
            return 1

        print(f"entry.png written: {byte_count} bytes, sha256 {output_hash}")
        return 0
    except OSError as error:
        print(f"Unable to copy picture.jpg to entry.png: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass
            except OSError as error:
                print(f"Unable to remove temporary file {temporary_path}: {error}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
