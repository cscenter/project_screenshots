import unittest
from tests.regression.precision_recall_calculator import PrecisionRecallCalculator


class TestPrecisionRecallCalculator(unittest.TestCase):

    def test_empty_pr_ctor_returns_none(self):
        pr_ctor = PrecisionRecallCalculator()
        self.assertIsNone(pr_ctor.precision())
        self.assertIsNone(pr_ctor.recall())
        self.assertIsNone(pr_ctor.fscore())

    def test_pr_ctor_handles_one_value_correctly(self):
        pr_ctor = PrecisionRecallCalculator()
        pr_ctor.add_true_positive()
        self.assertAlmostEqual(pr_ctor.precision(), 1., delta=1e-16)
        self.assertAlmostEqual(pr_ctor.recall(),    1., delta=1e-16)
        self.assertAlmostEqual(pr_ctor.fscore(),    1., delta=1e-16)

    def test_pr_ctor_handles_one_fp_correctly(self):
        pr_ctor = PrecisionRecallCalculator()
        pr_ctor.add_false_positive()
        self.assertAlmostEqual(pr_ctor.precision(), 0., delta=1e-16)
        self.assertIsNone(pr_ctor.recall())
        self.assertIsNone(pr_ctor.fscore())

    def test_pr_ctor_handles_one_fn_correctly(self):
        pr_ctor = PrecisionRecallCalculator()
        pr_ctor.add_false_negative()
        self.assertIsNone(pr_ctor.precision())
        self.assertAlmostEqual(pr_ctor.recall(), 0., delta=1e-16)
        self.assertIsNone(pr_ctor.fscore())

    def test_pr_ctor_handles_one_fn_and_one_fp_correctly(self):
        pr_ctor = PrecisionRecallCalculator()
        pr_ctor.add_false_negative()
        pr_ctor.add_false_positive()
        self.assertAlmostEqual(pr_ctor.precision(), 0., delta=1e-16)
        self.assertAlmostEqual(pr_ctor.recall(),    0., delta=1e-16)
        self.assertIsNone(pr_ctor.fscore())

    def test_pr_ctor_handles_many_values_correctly(self):
        pr_ctor = PrecisionRecallCalculator()
        for i in range(10):
            pr_ctor.add_true_positive()
        for i in range(5):
            pr_ctor.add_false_positive()
        for i in range(15):
            pr_ctor.add_false_negative()
        p = 10. / 15
        r = 10. / 25
        fscore = 2 * p * r / (p + r)

        self.assertAlmostEqual(pr_ctor.precision(), p, delta=1e-16)
        self.assertAlmostEqual(pr_ctor.recall(),    r, delta=1e-16)
        self.assertAlmostEqual(pr_ctor.fscore(),    fscore, delta=1e-16)
