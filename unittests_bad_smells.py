import unittest
import time, datetime

import bad_smells
import examples

class MarriageValidationTestCase(unittest.TestCase):
    def testMarriageBeforeDivorceSuccess(self):
        self.assertTrue(bad_smells.verifyMarriageBeforeDivorce(examples.exampleFamilyDivorced))

    def testMarriageBeforeDivorceFailure(self):
        self.assertFalse(bad_smells.verifyMarriageBeforeDivorce(examples.exampleImproperFamilyDivorced))

    def testMarriageBeforeDeathSuccess(self):
        self.assertTrue(bad_smells.marriageDeath(examples.exampleFamilyWithWidow))

    def testMarriageBeforeDeathFailure(self):
        self.assertFalse(bad_smells.marriageDeath(examples.exampleImproperFamilyWithWidow))

if __name__ == '__main__':
    bad_smells.processFile(bad_smells.GEDCOM_FILE)
    unittest.main()
