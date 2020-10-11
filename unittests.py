import unittest
import time, datetime

import parse
import verifier
import examples

class MarriageValidationTestCase(unittest.TestCase):
    def testMarriageBeforeDivorceSuccess(self):
        self.assertTrue(verifier.US04_verify_marriage_before_divorce(examples.exampleFamilyDivorced))

    def testMarriageBeforeDivorceFailure(self):
        self.assertFalse(verifier.US04_verify_marriage_before_divorce(examples.exampleImproperFamilyDivorced))

    def testMarriageBeforeDeathSuccess(self):
        self.assertTrue(verifier.US05_verify_marriage_before_death(examples.exampleFamilyWithWidow))

    def testMarriageBeforeDeathFailure(self):
        self.assertFalse(verifier.US05_verify_marriage_before_death(examples.exampleImproperFamilyWithWidow))

class AliveTooLongTestCase(unittest.TestCase):
    def setUp(self):
        self.verifier = verifier.US07_verify_death_before_150_years_old

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
        self.assertTrue(verifier.US01_verify_date_before_current_date(examples.exampleDateBeforeCurrentDate))

    def testDateEqualCurrentDate(self):
        self.assertFalse(verifier.US01_verify_date_before_current_date(examples.exampleDateEqualCurrentDate))

    def testDateAfterCurrentDate(self):
        self.assertFalse(verifier.US01_verify_date_before_current_date(examples.exampleDateAfterCurrentDate))

class BirthdayBeforeMarriageTestCase(unittest.TestCase):
    def testBirthdayBeforeMarriage(self):
        self.assertTrue(verifier.US02_verify_birth_before_marriage(examples.exampleBirthdayBeforeMarriage))

    def testBirthdayAfterMarriage(self):
        self.assertFalse(verifier.US02_verify_birth_before_marriage(examples.exampleBirthdayAfterMarriage))

    def testBirthdayEqualMarriage(self):
        self.assertFalse(verifier.US02_verify_birth_before_marriage(examples.exampleBirthdayEqualMarriage))

class MarriageBirthComparisonTestCase(unittest.TestCase):
    def setUp(self):
        self.verifier = verifier.US08_verify_birth_after_parents_marriage

    @unittest.skip("Takes a family when verifier implies it takes an individual")
    def test_normal_marriage(self):
        self.assertFalse(self.verifier(examples.exampleFamilyTogether))

    @unittest.skip("TODO, need test refactoring")
    def test_birth_before_marriage(self):
        verifier.individuals = {
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

    @unittest.skip("Old implementation relied on creating new dictionaries on the fly")
    def test_married_both_male(self):
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(
            MarriageGendersTestCase.families['@F1@']))

    def test_married_both_female(self):
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(
            MarriageGendersTestCase.families['@F2@']))

    def test_married_male_female_incorrect(self):
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(
            MarriageGendersTestCase.families['@F3@']))

    @unittest.skip("Old implementation relied on creating new dictionaries on the fly")
    def test_married_male_female_correct(self):
        self.assertTrue(verifier.US21_verify_marriage_gender_roles(
            MarriageGendersTestCase.families['@F4@']))

    def test_married_invalid_genders(self):
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(
            MarriageGendersTestCase.families['@F5@']))

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
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(
            self.families['@F1@']))

    @unittest.skip("Old implementation relied on creating new dictionaries on the fly")
    def test_between_siblings(self):
        self.assertFalse(verifier.US18_verify_marriage_not_siblings(
            self.families['@F2@']))

    def test_husband_parent_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(
            self.families['@F2@']))

    def test_wife_parent_na(self):
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(
            self.families['@F2@']))

    def test_both_parents_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(
            self.families['@F2@']))

class US12TestCase(unittest.TestCase):
    def test_old_parent(self):
        self.assertFalse(verifier.US12_verify_parents_not_too_old(
            examples.exampleFamilyWithTooYoungKid,
        ))
    
    def test_not_old_parent(self):
        self.assertTrue(verifier.US12_verify_parents_not_too_old(
            examples.exampleFamilyWithWidow
        ))       

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
        self.assertTrue(verifier.US11_verify_no_bigamy(self.familiesWithoutBigamy['@F1@']))
    def testNegativeBigamy(self):
        self.assertFalse(verifier.US11_verify_no_bigamy(self.familiesWithBigamy['@F2@']))

# Testing US35 & US36
class TestRecent30DayBornorDeath(unittest.TestCase):
    def test_verifyBirthAtRecent30Days(self):
        self.assertTrue(verifier.US35_verify_birth_at_recent_30_days(examples.examplePersonRecentBirth))

    def test_verifyDeathAtRecent30Days(self):
        self.assertTrue(verifier.US36_verify_death_at_recent_30_days(examples.examplePersonRecentDeath))

    def test_PersonNotRecentDeath(self):
        self.assertFalse(verifier.US36_verify_death_at_recent_30_days(examples.examplePersonNotRecentDeath))

if __name__ == '__main__':
    gedcom_file = 'cs555project03.ged'
    individuals, families = parse.parse_gedcom_file_03(gedcom_file)
    verifier.initialize_verifier(individuals, families)
    unittest.main()
