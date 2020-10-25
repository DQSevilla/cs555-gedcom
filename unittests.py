import unittest
import time, datetime
from unittest.mock import patch

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
    # US21 Correct gender for role

    @patch('verifier.find_individual')
    def test_married_both_male(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleWifeIncorrectGender,
                                            examples.exampleHusbandCorrectGender])
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(examples.exampleFamilyGay))

    @patch('verifier.find_individual')
    def test_married_both_female(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleWifeCorrectGender,
                                            examples.exampleHusbandIncorrectGender])
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(examples.exampleFamilyLesbian))

    @patch('verifier.find_individual')
    def test_married_male_female_incorrect(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleWifeIncorrectGender,
                                            examples.exampleHusbandIncorrectGender])
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(examples.exampleFamilyBothGendersIncorrect))

    @patch('verifier.find_individual')
    def test_married_male_female_correct(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleWifeCorrectGender,
                                            examples.exampleHusbandCorrectGender])
        self.assertTrue(verifier.US21_verify_marriage_gender_roles(examples.exampleFamilyCorrect))

    @patch('verifier.find_individual')
    def test_married_invalid_genders(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleIndividualInvalidGender,
                                            examples.exampleIndividualInvalidGender])
        self.assertFalse(verifier.US21_verify_marriage_gender_roles(examples.exampleFamilyInvalidGenders))

class MarriageBetweenSiblingsTestCase(unittest.TestCase):
    # US18 siblings should not marry

    @patch('verifier.find_individual')
    def test_not_between_siblings(self, mock_individual):
        mock_individual.side_effect = iter([examples.examplePersonAlive,
                                            examples.examplePersonAlive2])
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(examples.exampleFamilyTogether))

    @patch('verifier.find_individual')
    def test_between_siblings(self, mock_individual):
        mock_individual.side_effect = iter([examples.examplePersonSameParent1,
                                            examples.examplePersonSameParent2])
        self.assertFalse(verifier.US18_verify_marriage_not_siblings(examples.exampleFamilyBetweenSiblings))

    @patch('verifier.find_individual')
    def test_husband_parent_na(self, mock_individual):
        husband_no_parent = examples.examplePersonSameParent2
        husband_no_parent['child'] = 'NA'
        mock_individual.side_effect = iter([examples.examplePersonSameParent1,
                                            husband_no_parent])
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(examples.exampleFamilyTogether))

    @patch('verifier.find_individual')
    def test_wife_parent_na(self, mock_individual):
        wife_no_parent = examples.examplePersonSameParent1
        wife_no_parent['child'] = 'NA'
        mock_individual.side_effect = iter([wife_no_parent,
                                            examples.examplePersonSameParent2])
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(examples.exampleFamilyTogether))

    @patch('verifier.find_individual')
    def test_both_parents_na(self, mock_individual):
        wife_no_parent = examples.examplePersonSameParent1
        wife_no_parent['child'] = 'NA'
        husband_no_parent = examples.examplePersonSameParent2
        husband_no_parent['child'] = 'NA'
        mock_individual.side_effect = iter([wife_no_parent,
                                            husband_no_parent])
        self.assertTrue(verifier.US18_verify_marriage_not_siblings(examples.exampleFamilyTogether))

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

class DeadIndividualsTestCase(unittest.TestCase):
    # US29 List deceased

    def test_dead(self):
        self.assertTrue(verifier.US29_verify_deceased(examples.examplePersonDead))
        return

    def test_alive(self):
        self.assertFalse(verifier.US29_verify_deceased(examples.examplePersonAlive))
        return

class TestBirthAfterParentDeath(unittest.TestCase):

    def test_parents_alive(self):
        self.assertTrue(verifier.US09_verify_birth_before_parents_death(examples.exampleBornBeforeDeathParents))

    def test_birth_before_9_months_father_death(self):
        self.assertTrue(verifier.US09_verify_birth_before_parents_death(examples.exampleBornBefore9MonthsFather))

    def test_birth_after_mother_death(self):
        self.assertFalse(verifier.US09_verify_birth_before_parents_death(examples.exampleBornAfterDeathParents))

    def test_birth_after_9_months_father_death(self):
        self.assertFalse(verifier.US09_verify_birth_before_parents_death(examples.exampleBornAfter9MonthsFather))

class listLivingMarriedIndividualsTestCase(unittest.TestCase):
    # US30 List living married

    def testLivingMarried(self):
        self.assertTrue(verifier.US30_verify_living_married(examples.exampleIndividualAliveMarried))

    def testLivingUnmarried(self):
        self.assertFalse(verifier.US30_verify_living_married(examples.exampleIndividualAliveUnmarried))

    def testDeadMarried(self):
        self.assertFalse(verifier.US30_verify_living_married(examples.exampleIndividualDeadMarried))

    def testDeadUnmarried(self):
        self.assertFalse(verifier.US30_verify_living_married(examples.exampleIndividualDeadUnmarried))

<<<<<<< HEAD
class verifySiblingSpacingTestCase(unittest.TestCase):
    def onlyOneChild(self):
        self.assertTrue(verifier.US13_verify_sibling_spacing(examples.exampleFamilyOneChild))
=======
class US14TestCases(unittest.TestCase):
    def test_less_than_5(self):
        self.assertTrue(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthLessThan5, examples.exampleIndividualsDict))

    def test_equal_5(self):
        self.assertTrue(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthEqual5, examples.exampleIndividualsDict))

    def test_greater_than_5(self):
        self.assertFalse(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthGreaterThan5, examples.exampleIndividualsDict))


class UniqueNameAndBirthdateTestCase(unittest.TestCase):
    """US23: unique name and birthdays combinations"""
    def test_all_unique(self):
        self.assertTrue(verifier.US23_unique_name_and_birthdate())

    def test_not_all_unique(self):
        self.assertFalse(verifier.US23_unique_name_and_birthdate(individualsDict={
            '@I1@': {
                'id': '@I1@',
                'name': 'Alice /Trout/',
                'gender': 'F',
                'birthday': '2 DEC 1970',
                'age': 49,
                'alive': True,
                'death': 'NA',
                'child': '@F2@',
                'spouse': '@F1@',
            },
            '@I2@': {
                'id': '@I1@',
                'name': 'Alice /Trout/',
                'gender': 'F',
                'birthday': '2 DEC 1970',
                'age': 49,
                'alive': True,
                'death': 'NA',
                'child': '@F5@',
                'spouse': '@F1@',
            },
        }))

class US16TestCases(unittest.TestCase):
    def test_same_male_last_name(self):
        self.assertTrue(verifier.US16_verify_male_last_names(examples.exampleFamilyMalesWithSameLastName, examples.exampleIndividualsDict))

    def test_different_male_last_name(self):
        self.assertFalse(verifier.US16_verify_male_last_names(examples.exampleFamilyMalesWithoutSameLastName, examples.exampleIndividualsDict))

    def test_same_male_last_name_diff_female_last_name(self):
        self.assertTrue(verifier.US16_verify_male_last_names(examples.exampleFamilyMalesWithSameLastNameButDifferentFemale, examples.exampleIndividualsDict))
>>>>>>> 7e2ef6bfd8e7b755220fe02e4ca6472d9c3200c2

if __name__ == '__main__':
    gedcom_file = 'cs555project03.ged'
    individuals, families = parse.parse_gedcom_file_03(gedcom_file)
    verifier.initialize_verifier(individuals, families)
    unittest.main()