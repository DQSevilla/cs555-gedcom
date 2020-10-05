import unittest
import time, datetime

import project03
import examples

class MarriageValidationTestCase(unittest.TestCase):
    def testTimestamp(self):
        self.assertEqual(project03.gedcomDateToUnixTimestamp('01 JAN 1970'), time.mktime(datetime.datetime.strptime('1/1/1970', '%d/%m/%Y').timetuple()))
        self.assertTrue(project03.gedcomDateToUnixTimestamp('28 SEP 2020') == project03.gedcomDateToUnixTimestamp('28 SEP 2020'))
        self.assertTrue(project03.gedcomDateToUnixTimestamp('28 SEP 2020') > project03.gedcomDateToUnixTimestamp('28 SEP 2019'))

    def testMarriageBeforeDivorceSuccess(self):
        self.assertTrue(project03.verifyMarriageBeforeDivorce(examples.exampleFamilyDivorced))

    def testMarriageBeforeDivorceFailure(self):
        self.assertFalse(project03.verifyMarriageBeforeDivorce(examples.exampleImproperFamilyDivorced))

    def testMarriageBeforeDeathSuccess(self):
        self.assertTrue(project03.verifyMarriageBeforeDeath(examples.exampleFamilyWithWidow))

    def testMarriageBeforeDeathFailure(self):
        self.assertFalse(project03.verifyMarriageBeforeDeath(examples.exampleImproperFamilyWithWidow))


class AliveTooLongTestCase(unittest.TestCase):
    def setUp(self):
        self.verifier = project03.verifyDeathBefore150YearsOld

    def test_alive_less_than_150(self):
        self.assertTrue(self.verifier(examples.examplePersonAlive))

    def test_dead_less_than_150(self):
        self.assertTrue(self.verifier(examples.examplePersonDead))

    def test_dead_exactly_150(self):
        self.assertTrue(self.verifier(examples.examplePersonDead150))

    def test_alive_greater_than_150(self):
        self.assertFalse(self.verifier(examples.examplePersonAliveOver150))

    def test_dead_greater_than_150(self):
        self.assertFalse(self.verifier(examples.examplePersonDeadOver150))

class TestForBigamy(unittest.TestCase):
    def testMarriedPerson(self):
        self.assertFalse(noBigamy(examples.examplePersonMarried))
    def testNonMarriedPerson(self):
        self.assertTrue(noBigamy(examples.examplePersonNonMarried))
        
class TestForBigamy(unittest.TestCase):
    def setUp(self):
        self.familiesWithoutBigamy = {
            '@F1@': examples.exampleFamilyWithWidow, #Hus ID = 4, Wife ID = 5
            '@F2@': examples.exampleImproperFamilyDivorced, #Hus ID = 7, Wife ID = 3
            '@F3@': examples.exampleFamilyTogether #Hus ID = 2, Wife ID = 1
        }
        self.familiesWithBigamy = {
            '@F1@': examples.exampleFamilyWithWidow, #Hus ID = 4, Wife ID = 5
            '@F2@': examples.exampleImproperFamilyDivorced, #Hus ID = 7, Wife ID = 3
            '@F3@': examples.exampleFamilyDivorced #Hus ID = 7, Wife ID = 3
        }
    def testPositiveBigamy(self):
        self.assertTrue(project03.verifyNoBigamy(self.familiesWithoutBigamy['@F1@'], self.familiesWithoutBigamy))
    def testNegativeBigamy(self):
        self.assertFalse(project03.verifyNoBigamy(self.familiesWithBigamy['@F2@'], self.familiesWithBigamy))

if __name__ == '__main__':
    project03.processFile(project03.GEDCOM_FILE)
    unittest.main()
