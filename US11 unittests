import unittest
import examples
from project03 import noBigamy


class TestForBigamy(unittest.TestCase):

    def testMarriedPerson(self):
        self.assertFalse(noBigamy(examples.examplePersonMarried))
    def testNonMarriedPerson(self):
        self.assertTrue(noBigamy(examples.examplePersonNonMarried))


if __name__ == "__main__":
    unittest.main()
