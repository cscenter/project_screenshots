class AnalyserResult:
    def __init__(self, has_anomaly, info=None):
        self.has_anomaly = has_anomaly
        if info:
            self.info = info
        else:
            self.info = {}

    @staticmethod
    def with_anomaly(info=None):
        return AnalyserResult(True, info)

    @staticmethod
    def without_anomaly(info=None):
        return AnalyserResult(False, info)

    def update_info(self, key, value):
        self.info[key] = value

    def __nonzero__(self):
        return self.has_anomaly

    def __str__(self):
        result = ""
        if self.has_anomaly:
            result += "Detected the anomaly on the screenshot\n"
        else:
            result += "Did not detect the anomaly on the screenshot\n"
        if self.info:
            result += "Additional info: " + str(self.info) + "\n"
        return result
