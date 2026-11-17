import re
from pathlib import Path


class Rules:
    def __init__(self, raw_string: str):
        self.raw_string = raw_string
        self._pattern = re.compile(raw_string)

    def matches(self, strings: str):
        matches = self._pattern.finditer(strings)
        for match in matches:
            print(match)

    def verify(self, strings: str):
        verified = self._pattern.search(strings) is not None
        return verified


class PathFinder:
    def __init__(self):
        self.current_dir = Path(__file__).resolve()

    @property
    def cwd(self):
        return str(self.current_dir)

    def stack(self, path: str):
        absolute_path = self.current_dir / path
        return absolute_path


if __name__ == "__main__":
    text = "A1:B2"
    rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")

    path = PathFinder()
