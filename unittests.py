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
        
class TestMarriageAfter14(unittest.TestCase):
    def testBothOver14(self):
        self.assertTrue(project03.verifyMarriageAfter14(examples.exampleMarriage14YearsAfterBoth))
    def testHusbandOver14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriageHusbandOver14Years))
    def testWifeOver14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriageWifeOver14Years))
    def testBothUnder14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriage14YearsBeforeBoth))

if __name__ == '__main__':
    project03.processFile(project03.GEDCOM_FILE)
    unittest.main()
