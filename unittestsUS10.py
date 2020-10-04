import unittest
import examples
from project03 import marriageAfter14


class TestMarriageBefore14(unittest.TestCase):
    def testBothOver14(self):
        self.assertTrue(marriageAfter14(examples.exampleAgeOver14One, examples.exampleAgeOver14Two))
    def testOneOver14(self):
        self.assertFalse(marriageAfter14(examples.exampleAgeOver14One, examples.exampleAgeUnder14One))
    def testBothUnder14(self):
        self.assertFalse(marriageAfter14(examples.exampleAgeUnder14One, examples.exampleAgeUnder14Two))

if __name__ == "__main__":
    unittest.main()
