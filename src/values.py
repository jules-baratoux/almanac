import os
from pathlib import Path


def get_assets_dir() -> Path:
    try:
        value = os.environ["FLET_ASSETS_DIR"]
    except KeyError:
        return Path(__file__).with_name("assets")
    else:
        return Path(value)


class paths:
    assets = get_assets_dir()
    images = assets / "images"
