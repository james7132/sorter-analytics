import pyhash
import os
import os.path as path

HASHER = pyhash.xx_64()
SRC_DIR = path.dirname(path.realpath(__file__))
BASE_DIR = path.join(SRC_DIR, "sources/")
SOURCE_FORMAT = "sources/{}.txt"


class SorterSource():

    def __init__(self, entries):
        self.inverse = self._build_entries(entries)
        self.entries = {v: k for k, v in self.inverse.items()}

    @staticmethod
    def load_from(path):
        with open(path) as f:
            return SorterSource(f.read().splitlines())

    def get(self, key):
        return self.entries.get(key)

    def reverse_lookup(self, item):
        return self.inverse.get(item)

    def __contains__(self, key):
        return key in self.entries or key in self.inverse

    def _build_entries(self, entries):
        mapping = dict()
        for entry in entries:
            entry_hash = HASHER(entry)
            if entry_hash in mapping:
                elem = (entry, mapping[entry_hash], entry_hash)
                print('Hash collision found: %s vs %s (%d)' % elem)
            mapping[entry_hash] = entry
        return mapping


__files = (f for f in os.listdir(BASE_DIR)
           if path.isfile(path.join(BASE_DIR, f)))
__SOURCES__ = {f: SorterSource.load_from(path.join(BASE_DIR, f))
               for f in __files}

def get_source(source_id):
    return __SOURCES__.get(source_id)
