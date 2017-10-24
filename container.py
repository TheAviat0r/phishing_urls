import os

from global_config import ALGOTMP
import json


class ElementBase(object):

    def __init__(self, url, *args, **kwargs):
        self.url = url

    def encode_json(self):
        return json.dumps(vars(self))

    def __str__(self):
        args = vars(self)
        for key, value in args.items():
            output = '------------------------\n'
            output += '===> %s is %s\n' % (key, value)
            output += '------------------------\n'


class Container():
    path = ALGOTMP
    element_class = ElementBase
    elems = []

    def __init__(self, urls, *args, **kwargs):
        for url in urls:
            self.elems.append(self.element_class(url, args, kwargs))

    def get_data(self):
        raise NotImplementedError("Please Implement this method")

    def load_from_disc(self):
        with open(os.path.join(self.path, self.__class__.__name__+'_json_dump.json'), 'r') as f:
            json_elems = json.load(f)
        built_elems = []
        for json_elem in json_elems:
            values = []
            for key, value in json_elems.items():
                values.append(value)
            built_elems.append(self.element_class(*values))
        self.elems = built_elems

    def load_to_disc(self):
        json_elems = []
        for element in self.elems:
            json_elems.append(element.encode_json())
        with open(os.path.join(self.path, self.__class__.__name__+'_json_dump.json'), 'w') as f:
            json.dump(json_elems, f)

    def __str__(self):
        output = 'Temporary folder path: %s' % self.path
        for element in self.elems:
            output += element.__str__()
