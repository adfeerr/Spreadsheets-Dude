import re


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
        pass


class EnvVar:
    pass


if __name__ == "__main__":
    text = "A1:B2"
    rules = Rules(r"[A-Z]\d{1,4}+:[A-Z]\d{1,3}")
