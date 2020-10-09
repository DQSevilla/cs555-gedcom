import unittest
import time, datetime

import good_smells
import examples

class MarriageValidationTestCase(unittest.TestCase):
    def testMarriageBeforeDivorceSuccess(self):
        self.assertTrue(good_smells.verifyMarriageBeforeDivorce(examples.exampleFamilyDivorced))

    def testMarriageBeforeDivorceFailure(self):
        self.assertFalse(good_smells.verifyMarriageBeforeDivorce(examples.exampleImproperFamilyDivorced))

    def testMarriageBeforeDeathSuccess(self):
        self.assertTrue(good_smells.verifyMarriageBeforeDeath(examples.exampleFamilyWithWidow))

    def testMarriageBeforeDeathFailure(self):
        self.assertFalse(good_smells.verifyMarriageBeforeDeath(examples.exampleImproperFamilyWithWidow))

if __name__ == '__main__':
    good_smells.processFile(good_smells.GEDCOM_FILE)
    unittest.main()
