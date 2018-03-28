

class PrecisionRecallCalculator:
    def __init__(self, test_name="sample_test"):
        self.TP = 0.
        self.TN = 0.
        self.FP = 0.
        self.FN = 0.
        self.test_name = test_name

    # expected: bool
    def expected(self, expected):
        return PRProxy(self, expected)

    def add_TP(self):
        self.TP += 1

    def add_TN(self):
        self.TN += 1

    def add_FP(self):
        self.FP += 1

    def add_FN(self):
        self.FN += 1

    def recall(self):
        if self.TP + self.FN == 0:
            return -1
        else:
            return self.TP / (self.TP + self.FN)

    def precision(self):
        if self.TP + self.FP == 0:
            return -1
        else:
            return self.TP / (self.TP + self.FP)

    def fscore(self):
        p = self.precision()
        r = self.recall()
        if p == -1 or r == -1:
            return -1
        else:
            return 2 * p * r / (p + r)

    def __str__(self):
        str = \
        "Statistics for {0}\n".format(self.test_name) +\
        "-" * len(self.test_name) + "\n" +\
        "{0:20s}: {1:.5f}\n".format("Precision: ",        self.precision()) +\
        "{0:20s}: {1:.5f}\n".format("Recall: ",           self.recall()) +\
        "{0:20s}: {1:.5f}\n".format("FScore: ",           self.fscore()) +\
        "{0:20s}: {1:.5f}\n".format("True positive: ",    self.TP) +\
        "{0:20s}: {1:.5f}\n".format("True negative: ",    self.TN) +\
        "{0:20s}: {1:.5f}\n".format("False positive: ",   self.FP) +\
        "{0:20s}: {1:.5f}\n".format("False negative: ",   self.FN)

        return str

class PRProxy:
    # prctor: PrecisionRecallCalculator
    # expected: bool
    def __init__(self, prctor, expected):
        self.expected = expected
        self.prctor = prctor

    # found: bool
    def found(self, found):
        if self.expected:
            if found:
                self.prctor.add_TP()
            else:
                self.prctor.add_FN()
        else:
            if found:
                self.prctor.add_FP()
            else:
                self.prctor.add_TN()
