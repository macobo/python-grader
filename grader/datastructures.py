from .utils import import_module

class OrderedTestcases:
    " Class that acts like a ordered dictionary, with removal and reset"
    def __init__(self):
        self.clear()

    def clear(self):
        self.cases = {}
        self.order = []

    def _indexOf(self, name):
        return self.order.index(name)

    def add(self, name, value):
        #assert name not in self.order
        self.cases[name] = value
        self.order.append(name)

    def remove(self, name):
        self.order.remove(name)
        self.cases.pop(name)

    def rename(self, old_name, new_name):
        if old_name not in self.cases:
            raise ValueError('Old name {} does not exist in keys.'.format(old_name))
        if new_name in self.cases:
            raise ValueError('New name {} already exists in keys.'.format(new_name))

        self.order[self._indexOf(old_name)] = new_name
        self.cases[new_name] = self.cases[old_name]
        self.cases.pop(old_name)

    def load_cases(self, module_path):
        self.clear()
        import_module(module_path)

    @property
    def names(self):
        return self.order
    
    def test_names(self):
        return 

    def __getitem__(self, name):
        return self.cases[name]

    def __contains__(self, name):
        return name in self.cases

    def __iter__(self):
        return ((o, self.cases[o]) for o in self.order)

    def __len__(self):
        return len(list(x for x in self))