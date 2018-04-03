class AnalyserResult:
    def __init__(self, has_anomaly, analyser_type=None, description=None):
        self.has_anomaly = has_anomaly
        self.analyser_type = analyser_type
        self.description = description

    def __nonzero__(self):
        return self.has_anomaly

    def __str__(self):
        result = str(self.analyser_type)
        if self.has_anomaly:
            result += " detected the anomaly on the screenshot"
            if self.description:
                result += " : " + str(self.description)
            result += "\n"
        else:
            result += " did not detect the anomaly on the screenshot\n"
        return result
