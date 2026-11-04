from __future__ import annotations

import hashlib
import itertools
from collections.abc import Sequence
from operator import floordiv
from pathlib import Path

import PIL.Image
from PIL.ExifTags import Base

import project
from dispatch import overload
from values import paths


class Size:
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    @overload
    def __floordiv__(self, other: Size):
        return Size(*itertools.starmap(floordiv, zip(self, other)))

    @overload
    def __floordiv__(self, other: int):
        return Size(self.width // other, self.height // other)

    def __iter__(self):
        yield self.width
        yield self.height

    @overload
    def __eq__(self, other: Size):
        return self.width == other.width and self.height == other.height

    @overload
    def __eq__(self, other: Sequence[int]):
        for a, b in zip(self, other):
            if a != b:
                return False
        else:
            return True

    def __str__(self):
        return f'{self.width}×{self.height}'

    def cover(self, width: int, height: int):
        """Return a new size that covers the given width and height."""
        area = Size(width, height)
        divisors = self // area
        divisor = min(*divisors)
        if divisor <= 0:
            raise ValueError(f'{area} > {self}')
        return self // divisor


def md5(fp):
    h = hashlib.md5()
    for chunk in iter(lambda: fp.read(1 << 20), b""):
        h.update(chunk)
    return h


class Copy:
    def __init__(self, file, original, width: int, height: int, quality: int, parent: Path, suffix: str):
        path = Path(file.name)
        self.original = original
        self.quality = quality
        self.exif = original.getexif()
        self.exif[Base.Software] = f'{Path(__file__).name}, {quality=}'
        try:
            self.exif[Base.OriginalRawFileName]
        except KeyError:
            self.exif[Base.OriginalRawFileName] = path.resolve().relative_to(project.root).as_posix()

        try:
            self.exif[Base.OriginalRawFileDigest]
        except KeyError:
            self.exif[Base.OriginalRawFileDigest] = md5(file).digest()

        self.path = parent / path.with_suffix(suffix).name
        self.size = Size(*original.size).cover(width, height)

    def exists(self) -> bool:
        try:
            with PIL.Image.open(self.path) as image:
                for key, value in self.exif.items():
                    try:
                        actual = image.getexif()[key]
                    except KeyError:
                        return False
                    if actual != value:
                        return False
                else:
                    return image.size == self.size
        except FileNotFoundError:
            return False

    def create(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        (
            self.original.convert("RGB")
            .resize(size=self.size, resample=PIL.Image.Resampling.LANCZOS, reducing_gap=3)
            .save(self.path, exif=self.exif, quality=self.quality)
        )


def export(source: Path, destination: Path, suffix: str, width: int, height: int, quality: int):
    with open(source, 'rb') as file:
        with PIL.Image.open(file) as image:
            copy = Copy(file, image, width, height, quality, destination, suffix)
            if not copy.exists():
                copy.create()
                print(f'{source.relative_to(project.root).as_posix()} -> {copy.path.relative_to(project.root)}')


def main():
    for path in project.raw_images.iterdir():
        if path.is_file():
            export(path, paths.images, ".jpg", width=600, height=300, quality=95)


if __name__ == '__main__':
    main()
