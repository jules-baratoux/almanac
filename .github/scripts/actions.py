import re
import sys
from pathlib import Path


def export(path: str, *keys: str):
    """Print `keys` in `path` with their values using shell syntax."""
    keys_or = '|'.join(keys)
    pattern = re.compile(rf'^({keys_or}):\s*(.*)$')
    with Path(path).open(encoding='utf-8') as file:
        for line in file:
            if match := pattern.match(line):
                key, value = match.groups()
                print(f"{key}={value}")


if __name__ == '__main__':
    self, command, *args = sys.argv
    globals()[command](*args)
