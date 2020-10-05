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

class DateBeforeCurrentDateTestCase(unittest.TestCase):
    def testDateBeforeCurrentDate(self):
        self.assertTrue(project03.verifyDateBeforeCurrentDate(examples.exampleDateBeforeCurrentDate))

    def testDateEqualCurrentDate(self):
        self.assertFalse(project03.verifyDateBeforeCurrentDate(examples.exampleDateEqualCurrentDate))

    def testDateAfterCurrentDate(self):
        self.assertFalse(project03.verifyDateBeforeCurrentDate(examples.exampleDateAfterCurrentDate))

class BirthdayBeforeMarriageTestCase(unittest.TestCase):
    def testBirthdayBeforeMarriage(self):
        self.assertTrue(project03.verifyBirthBeforeMarriage(examples.exampleBirthdayBeforeMarriage))

    def testBirthdayAfterMarriage(self):
        self.assertFalse(project03.verifyBirthBeforeMarriage(examples.exampleBirthdayAfterMarriage))

    def testBirthdayEqualMarriage(self):
        self.assertFalse(project03.verifyBirthBeforeMarriage(examples.exampleBirthdayEqualMarriage))

class MarriageBirthComparisonTestCase(unittest.TestCase):
    def setUp(self):
        self.verifier = project03.verifyBirthAfterParentsMarriage

    def test_normal_marriage(self):
        self.assertFalse(self.verifier(examples.exampleFamilyTogether))

    @unittest.skip("TODO, need test refactoring")
    def test_birth_before_marriage(self):
        project03.individuals = {
            '@I4@': {
                'id': '@I4@',
                'name': 'Serafina /Russo/',
                'gender': 'F',
                'birthday': '2 DEC 1970',
                'age': 49,
                'alive': True,
                'death': 'NA',
                'child': 'NA',
                'spouse': 'NA'
            }
        }
        self.assertTrue(self.verifier(examples.exampleBirthBeforeMarriageFamily))

class MarriageGendersTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.families = {
            '@F1@': examples.exampleFamilyGay,
            '@F2@': examples.exampleFamilyLesbian,
            '@F3@': examples.exampleFamilyBothGendersIncorrect,
            '@F4@': examples.exampleFamilyCorrect,
            '@F5@': examples.exampleFamilyInvalidGenders
        }

        cls.individuals = {
            '@I1@': examples.exampleWifeIncorrectGender,
            '@I2@': examples.exampleHusbandCorrectGender,
            '@I3@': examples.exampleWifeCorrectGender,
            '@I4@': examples.exampleHusbandIncorrectGender,
            '@I5@': examples.exampleIndividualInvalidGender
        }

    def test_married_both_male(self):
        self.assertFalse(project03.ensureMarriageGenderRoles(
            MarriageGendersTestCase.families['@F1@'],
            MarriageGendersTestCase.individuals))

    def test_married_both_female(self):
        self.assertFalse(project03.ensureMarriageGenderRoles(
            MarriageGendersTestCase.families['@F2@'],
            MarriageGendersTestCase.individuals))

    def test_married_male_female_incorrect(self):
        self.assertFalse(project03.ensureMarriageGenderRoles(
            MarriageGendersTestCase.families['@F3@'],
            MarriageGendersTestCase.individuals))

    def test_married_male_famele_correct(self):
        self.assertTrue(project03.ensureMarriageGenderRoles(
            MarriageGendersTestCase.families['@F4@'],
            MarriageGendersTestCase.individuals))

    def test_married_invalid_genders(self):
        self.assertFalse(project03.ensureMarriageGenderRoles(
            MarriageGendersTestCase.families['@F5@'],
            MarriageGendersTestCase.individuals))

class MarriageBetweenSiblingsTestCase(unittest.TestCase):

    def setUp(self):
        self.families = {
            '@F1@': examples.exampleFamilyTogether,
            '@F2@': examples.exampleFamilyBetweenSiblings

        }

        self.individuals = {
            '@I1@': examples.examplePersonAlive,
            '@I2@': examples.examplePersonAlive2,
            '@I3@': examples.examplePersonSameParent1,
            '@I4@': examples.examplePersonSameParent2,
        }

    def test_not_between_siblings(self):
        self.assertTrue(project03.verifyMarriageNotSiblings(
            self.families['@F1@'],
            self.individuals))

    def test_between_siblings(self):
        self.assertFalse(project03.verifyMarriageNotSiblings(
            self.families['@F2@'],
            self.individuals))

    def test_husband_parent_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.assertTrue(project03.verifyMarriageNotSiblings(
            self.families['@F2@'],
            self.individuals))

    def test_wife_parent_na(self):
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(project03.verifyMarriageNotSiblings(
            self.families['@F2@'],
            self.individuals))

    def test_both_parents_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(project03.verifyMarriageNotSiblings(
            self.families['@F2@'],
            self.individuals))

class US12TestCase(unittest.TestCase):
    def test_old_parent(self):
        self.assertFalse(project03.verifyParentsNotTooOld(
            examples.exampleFamilyWithTooYoungKid,
        ))
    
    def test_not_old_parent(self):
        self.assertTrue(project03.verifyParentsNotTooOld(
            examples.exampleFamilyWithWidow
        ))
class TestMarriageAfter14(unittest.TestCase):
    def testBothOver14(self):
        self.assertTrue(project03.verifyMarriageAfter14(examples.exampleMarriage14YearsAfterBoth))
    def testHusbandOver14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriageHusbandOver14Years))
    def testWifeOver14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriageWifeOver14Years))
    def testBothUnder14(self):
        self.assertFalse(project03.verifyMarriageAfter14(examples.exampleMarriage14YearsBeforeBoth))


#Testing US35 & US36
class TestRecent30DayBornorDeath(unittest.TestCase):
    def test_verifyBirthAtRecent30Days(self):
        self.assertTrue(CS555.verifyBirthAtRecent30Days(examples.examplePersonRecentBirth))

    def test_verifyDeathAtRecent30Days(self):
        self.assertTrue(CS555.verifyDeathAtRecent30Days(examples.examplePersonRecentDeath))

    def test_PersonNotRecentDeath(self):
        self.assertFalse(CS555.verifyDeathAtRecent30Days(examples.examplePersonNotRecentDeath))

if __name__ == '__main__':
    project03.processFile(project03.GEDCOM_FILE)
    unittest.main()
