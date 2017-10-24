from container import Container


class Algorithm():
    suspicious_container_class = Container
    urls = []

    def __init__(self, filename, *args, **kwargs):
        with open(filename, 'r') as f:
            self.urls = list(f)
        self.results = []

    def get_suspicious_data(self, *args, **kwargs):
        container = self.suspicious_container_class(self.urls, args, kwargs)
        container.get_data()
        return container.elems

    def get_answer(self, suspect):
        raise NotImplementedError("Please Implement this method")

    def run(self, *args, **kwargs):
        for suspect in self.get_suspicious_data(args, kwargs):
            self.results.append((suspect, self.get_answer(suspect)))

    def answers(self):
        for elem in self.results:
            print(elem[0].__str__())
            if elem[1] == 0:
                print('Not phishing')
            else:
                print('Phishing')

    def __str__(self):
        pass
