import os
import sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def instance_getter(to_count: list, instance: object) -> int:
    count = []
    for obj in to_count:
        if isinstance(obj, instance):
            count.append(obj)
    return count
