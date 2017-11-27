from bcolors import bcolors
from container import Container
from global_config import BAD_SAMPLE_CONSTANT

import json


class Algorithm(object):
    """Базовый класс алгоритма, наследуемся от него"""

    suspicious_container_class = Container
    name = "Abstract algo"

    '''Берёт список урлов из json + формирует переменную будущих результатов'''

    def __init__(self, urls_list, *args, **kwargs):
        self.urls = urls_list

        print("[x] URL LIST RECEIVED: ")
        print(urls_list)

        self.results = []

    '''Формирует контейнер'''

    def get_suspicious_data(self, *args, **kwargs):
        container = self.suspicious_container_class(self.urls, *args, **kwargs)
        container.get_data()
        return container

    '''Оснвная функция, которую надо реализовать, выдаёт ответ, например, число'''

    def get_answer(self, suspect):
        raise NotImplementedError("Please Implement this method")

    '''Формирует резлуьтат, по ходу выполнения в контейнер собираются данные и для каждого элемента'''
    '''в контейнере вызывается функция get_answer.'''
    '''Ответ в итоге это список кортежей (элемент контейнера, ответ)'''

    def run(self, *args, **kwargs):
        print("%s working" % self.name)
        # print('[*] URLS SUPPLIED: ' + str(self.urls))
        container = self.get_suspicious_data(*args, **kwargs)
        for suspect in container.elems:
            print("Process %s" % suspect.url)
            self.results.append((suspect, self.get_answer(suspect)))
        container.cleanup()
        print("\n")

    '''Выводит ответ в удобоваримом формате'''

    def answers(self):
        '''
        output = "====================\n"
        for elem in self.results:
            output += elem[0].url
            if elem[1] == 0:
                output += " --->" + bcolors.BOLD + bcolors.OKGREEN + " Not phishing" + bcolors.ENDC + bcolors.ENDC + "\n"
            if elem[1] == 1:
                output += " --->" + bcolors.BOLD + bcolors.FAIL + " Phishing" + bcolors.ENDC + bcolors.ENDC + "\n"
            if elem[1] == BAD_SAMPLE_CONSTANT:
                output += " --->" + bcolors.BOLD + bcolors.WARNING + " Bad sample" + bcolors.ENDC + bcolors.ENDC + "\n"
        output += "====================\n"
        print(output)
        '''

        return self.results

    def __str__(self):
        pass
