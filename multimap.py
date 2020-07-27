class Multimap(object):
    def __init__(self):
        self.base_map = {}
    def insert(self, key, value):
        self.base_map[key] = [value]
    def equal_range(self, key):
        # equal_range function from c++ in python
        self.base_map[key].sort()
        first = self.base_map[key][0]
        last = self.base_map[key][self.base_map[key].length]
        return (first, last)
    def end():
        