import json
import sys
from hashlib import sha1

if sys.version_info < (3,0):
    from io import open


class FileCoverage:
    def __init__(self, file_node):
        self.file_node = file_node
        self.__process()

    def payload(self):
        return {
            "name": self.__filename(),
            "blob_id": self.__blob(),
            "covered_strength": self.__covered_strength(),
            "covered_percent": self.__covered_percent(),
            "coverage": json.dumps(self.__coverage()),
            "line_counts": self.__line_counts()
        }

    def __process(self):
        self.total = len(self.__line_nodes())
        self.hits = 0
        self.covered = 0
        self.missed = 0

        for line_node in self.__line_nodes():
            hits = int(line_node.get("hits"))

            if hits > 0:
                self.covered += 1
                self.hits += hits
            else:
                self.missed += 1

    def __line_nodes(self):
        return self.file_node.findall("lines/line")

    def __blob(self):
        contents = open(self.__filename(), "r", encoding="utf-8-sig").read()
        header = "blob " + str(len(contents)) + "\0"

        return sha1((header + contents).encode("utf-8")).hexdigest()

    def __filename(self):
        return self.file_node.get("filename")

    def __rate(self):
        return self.file_node.get("line-rate")

    def __covered_strength(self):
        return self.__guard_division(self.hits, self.covered)

    def __num_lines(self):
        return sum(1 for line in open(self.__filename()))

    def __covered_percent(self):
        return self.__guard_division(self.covered, self.total)

    def __guard_division(self, dividend, divisor):
        if (divisor > 0):
            return dividend / float(divisor)
        else:
            return 0.0

    def __coverage(self):
        coverage = [None] * self.__num_lines()

        for line_node in self.__line_nodes():
            index = int(line_node.get("number")) - 1
            hits = int(line_node.get("hits"))

            coverage[index] = hits

        return coverage

    def __line_counts(self):
        return {
            "total": self.total,
            "covered": self.covered,
            "missed": self.missed
        }
