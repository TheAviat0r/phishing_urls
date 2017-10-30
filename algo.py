from container import Container
from global_config import BAD_SAMPLE_CONSTANT


class Algorithm():
    suspicious_container_class = Container
    urls = []

    def __init__(self, filename, *args, **kwargs):
        with open(filename, 'r') as f:
            self.urls = list(f)
        self.results = []

    def get_suspicious_data(self, *args, **kwargs):
        container = self.suspicious_container_class(self.urls, *args, **kwargs)
        container.get_data()
        return container

    def get_answer(self, suspect):
        raise NotImplementedError("Please Implement this method")

    def run(self, *args, **kwargs):
        container = self.get_suspicious_data(*args, **kwargs)
        for suspect in container.elems:
            self.results.append((suspect, self.get_answer(suspect)))
        container.cleanup()

    def answers(self):
        for elem in self.results:
            print(elem[0])
            if elem[1] == -1:
                print('Not phishing')
            if elem[1] == 1:
                print('Phishing')
            if elem[1] == BAD_SAMPLE_CONSTANT:
                print('Bad sample, cannot say anything')

    def __str__(self):
        pass
