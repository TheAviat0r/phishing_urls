import os

import shutil

from global_config import ALGOTMP
import json


class ElementBase(object):
    """Базовый класс элемента контейнера"""

    '''Как минимум содержит url'''
    def __init__(self, url, *args, **kwargs):
        self.url = url

    '''Нужно для выгрузки на диск'''
    def encode_json(self):
        return json.dumps(vars(self))

    def __str__(self):
        args = vars(self)
        output = '====================\n'
        output += self.__class__.__name__ + ' object\n'
        for key, value in args.items():
            output += '------------------------\n'
            output += '===> %s is %s\n' % (key, value)
            output += '------------------------\n'
        output += '===================='
        return output


class Container(object):
    """Базовый класс контейнера"""

    path = ALGOTMP
    element_class = ElementBase

    '''Инициализирует список элементов контейнера, создаёт нужные папки'''
    def __init__(self, urls, *args, **kwargs):
        self.elems = []
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for url in urls:
            self.elems.append(self.element_class(url, *args, **kwargs))

    '''Достаёт нужные данные, например, скриншоты, доформировывает контейнер перед отправкой на проверку алгоритму'''
    '''Возможно, стоит его убрать, и сделать получение данных просто в инициализации элементов контейнера,'''
    '''как это сейчас сделано в алгоритме с изображениями'''
    def get_data(self):
        raise NotImplementedError("Please Implement this method")

    '''Загружает данные на диск в json формате, загатовка для будущих выгрузок в базу'''
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

    '''Грузит данные с диска'''
    def load_to_disc(self):
        json_elems = []
        for element in self.elems:
            json_elems.append(element.encode_json())
        with open(os.path.join(self.path, self.__class__.__name__+'_json_dump.json'), 'w') as f:
            json.dump(json_elems, f)

    '''Чистит временные файлы'''
    def cleanup(self):
        shutil.rmtree(self.path)

    def __str__(self):
        output = 'Temporary folder path: %s' % self.path
        for element in self.elems:
            output += element.__str__()
        return output

