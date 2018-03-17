class AnalyserResults(object):
    def __init__(self):
        self.results = []

    def print_results(self):
        if len(self.results) == 0:
            print("No anomalies found on this screenshot.")
            return
        for el in self.results:
            print(el)
    def append(self, el):
        self.results.append(el)