import unittest
import time, datetime
from unittest.mock import patch

import parse
import verifier
import examples
import utils

class MarriageValidationTestCase(unittest.TestCase):
    def testMarriageBeforeDivorceSuccess(self):
        self.assertTrue(verifier.US04_verify_marriage_before_divorce(examples.exampleFamilyDivorced))

    def testMarriageBeforeDivorceFailure(self):
        self.assertFalse(verifier.US04_verify_marriage_before_divorce(examples.exampleImproperFamilyDivorced))

    def testMarriageBeforeDeathSuccess(self):
        self.assertTrue(verifier.US05_verify_marriage_before_death(examples.exampleFamilyWithWidow))

    def testMarriageBeforeDeathFailure(self):
        self.assertFalse(verifier.US05_verify_marriage_before_death(examples.exampleImproperFamilyWithWidow))

class NoMarriageToDescendantsTestCase(unittest.TestCase):
    def setUp(self):
        self.individualsDict = {
            '@I1@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F2@',
            'spouse': '@F1@'
            },
            '@I2@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F1@'
            },
            '@I3@':{
            'id': '@I3@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F1@',
            'spouse': '@F5@'
            }
        }

        self.familiesDict = {
            '@F1@':{
            'id': '@F1@',
            'married': '14 MAY 1994',
            'divorced': 'NA',
            'husbandId': '@I2@',
            'husbandName': 'George /Salmon/',
            'wifeId': '@I1@',
            'wifeName': 'Alice /Trout/',
            'children': ['@I2@']
            },
            '@F5@':{
            'id': '@F5@',
            'married': '14 MAY 1994',
            'divorced': 'NA',
            'husbandId': '@I4@',
            'husbandName': 'George /Salmon/',
            'wifeId': '@I5@',
            'wifeName': 'Alice /Trout/',
            'children': []
            }
        }

    def test_marriage_to_decendants(self):
        self.assertFalse(verifier.US17_verify_no_marriage_to_descendants(self.individualsDict['@I1@'], self.individualsDict, self.familiesDict))

    def test_no_marriage_to_decendants(self):
        self.familiesDict['@F1@']['children'] = ['@I3@']
        self.assertTrue(verifier.US17_verify_no_marriage_to_descendants(self.individualsDict['@I1@'], self.individualsDict, self.familiesDict))

class AuntsAndUnclesTestCase(unittest.TestCase):
    def setUp(self):
        self.individualsDict = {
            '@I1@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F2@',
            'spouse': '@F1@'
            },
            '@I2@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F1@'
            },
            '@I3@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F55@',
            'spouse': '@F4@'
            },
            '@I4@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F3@'
            }
        }

        self.familiesDict = {
            '@F1@':{
            'id': '@F1@',
            'married': '14 MAY 1994',
            'divorced': 'NA',
            'husbandId': '@I2@',
            'husbandName': 'George /Salmon/',
            'wifeId': '@I33@',
            'wifeName': 'Alice /Trout/',
            'children': ['@I3@', '@I16@']
            },
            '@F2@':{
            'id': '@F2@',
            'married': '14 MAY 1994',
            'divorced': 'NA',
            'husbandId': '@I7@',
            'husbandName': 'Guy /Salmon/',
            'wifeId': '@I90@',
            'wifeName': 'Alice /Trout/',
            'children': ['@I1@', '@I4@']
            },
            '@F3@':{
            'id': '@F3@',
            'married': '14 MAY 1994',
            'divorced': 'NA',
            'husbandId': '@I66@',
            'husbandName': 'George /Salmon/',
            'wifeId': '@I5@',
            'wifeName': 'Alice /Trout/',
            'children': ['@I33@', '@I44@']
            }
        }

    def test_aunts_and_uncles(self):
        self.assertFalse(verifier.US20_verify_aunts_and_uncles(self.individualsDict['@I1@'], self.individualsDict, self.familiesDict))

    def test_no_aunts_and_uncles(self):
        self.familiesDict['@F1@']['wifeId'] = '@I1@'
        self.assertTrue(verifier.US20_verify_aunts_and_uncles(self.individualsDict['@I1@'], self.individualsDict, self.familiesDict))

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



class listMultipleBirths(unittest.TestCase):
    # US32 List multiple births

    def setUp(self):
        self.family_twins = {'children': ['@I1@', '@I2@']}
        self.family_normal = {'children': ['@I1@', '@I2@']}
        self.family_no_children = {'children': []}

    @patch('verifier.find_individual')
    def testMultipleBirths(self, mock_individual):
        mock_individual.side_effect = iter([examples.examplePersonSameBirthday1,
                                            examples.examplePersonSameBirthday2])
        self.assertEqual(verifier.US32_get_multiple_births(self.family_twins), [['@I1@', '@I2@']])

    @patch('verifier.find_individual')
    def testSingleBirths(self, mock_individual):
        mock_individual.side_effect = iter([examples.examplePersonDifferentBirthday1,
                                            examples.examplePersonDifferentBirthday2])
        self.assertEqual(verifier.US32_get_multiple_births(self.family_normal), [])

    def testNoBirths(self):
        self.assertEqual(verifier.US32_get_multiple_births(self.family_no_children), [])


class verifySiblingSpacingTestCase(unittest.TestCase):
    def onlyOneChild(self):
        self.assertTrue(verifier.US13_verify_sibling_spacing(examples.exampleFamilyOneChild, examples.exampleIndividualsDict))
    def twinFamily(self):
        self.assertTrue(verifier.US13_verify_sibling_spacing(examples.exampleTwinFamily, examples.exampleIndividualsDict))
    def spacedFamily(self):
        self.assertTrue(verifier.US13_verify_sibling_spacing(examples.exampleSpacedFamily, examples.exampleIndividualDict))
    def nonSpacedFamily(self):
        self.assertFalse(verifier.US13_verify_sibling_spacing(examples.exampleNonSpacedFamily, examples.exampleIndividualsDict))


class verifyLessThan15SiblingsTestCase(unittest.TestCase):
    #US15 less than 15 siblings
    def testLess15(self):
        self.assertTrue(verifier.US15_verify_fewer_than_15_siblings(examples.exampleFamilyLesbian))
    def testOver15(self):
        self.assertFalse(verifier.US15_verify_fewer_than_15_siblings(examples.exampleFamilyOver15Siblings))
class US14TestCases(unittest.TestCase):
    def test_less_than_5(self):
        self.assertTrue(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthLessThan5, examples.exampleIndividualsDict))

    def test_equal_5(self):
        self.assertTrue(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthEqual5, examples.exampleIndividualsDict))

    def test_greater_than_5(self):
        self.assertFalse(verifier.US14_verify_multiple_births(examples.exampleFamilyChildrenBirthGreaterThan5, examples.exampleIndividualsDict))

class US28TestCases(unittest.TestCase):
    def runSiblingOrdering(self):
        raised = False
        try:
            verifier.US28_order_siblings(examples.exampleSiblingOrdering)
        except:
            raised = True
        self.assertFalse(raised, "Exception raised unexpectedly")

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

class US33AndUS34TestCases(unittest.TestCase):
    #def setUp(self):
    @patch('verifier.find_individual')
    @patch('verifier.find_family')
    def test_orphans(self, mock_family, mock_individual):
        mock_family.side_effect = iter([examples.exampleOrphanFamily])
        mock_individual.side_effect = iter([examples.exampleFatherOfOrphan,
                                            examples.exampleMatherOfOrphan])
        self.assertTrue(verifier.US33_verify_orphans(examples.exampleOrphan))

    @patch('verifier.find_individual')
    def test_large_age_differences_couples(self, mock_individual):
        mock_individual.side_effect = iter([examples.exampleFatherOfOrphan,
                                            examples.exampleMatherOfOrphan])
        self.assertFalse(verifier.US34_verify_large_age_differences_couples(examples.exampleOrphanFamily))

class US38PersonBirthdayInNext30DaysTestCases(unittest.TestCase):
    def test_birthday(self):
        self.assertTrue(verifier.US38_verify_birthday_in_the_next_30_days(examples.examplePersonBirthdayInNext30Days))
    def test_not_recent_birthday(self):
        self.assertFalse(verifier.US38_verify_birthday_in_the_next_30_days(examples.examplePersonRecentDeath))

class US39UpcomingAnniversary(unittest.TestCase):
    def upcomingAnniversary(self):
        self.assertTrue(verifier.US39_verify_upcoming_anniversaries_30_days(examples.exampleIncomingAnniversary, examples.exampleAnniversaryDict))
    def noUpcomingAnniversary(self):
        self.assertFalse(verifier.US39_verify_upcoming_anniversaries_30_days(examples.exampleFarAnniversary, examples.exampleAnniversaryDict))

class US46MaleFemaleRatioTestCase(unittest.TestCase):
    def setUp(self):
        self.individualsDict = {
            '@I1@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F2@',
            'spouse': '@F1@'
            },
            '@I2@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F1@'
            },
            '@I3@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F55@',
            'spouse': '@F4@'
            },
            '@I4@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F3@'
            }
        }
    def test_equal_ratio(self):
        self.assertEqual(verifier.US46_male_female_ratio(self.individualsDict), (50.0, 50.0))

    def test_different_ratio(self):
        self.individualsDict['@I4@']['gender'] = 'F'
        self.assertEqual(verifier.US46_male_female_ratio(self.individualsDict), (25.0, 75.0))

class US24UniqueFamiliesBySpouseTestCase(unittest.TestCase):
    def setUp(self):
        self.familiesDictDup = {
            '@F2@': {
                'id': '@F2@',
                'married': '2 JAN 1970',
                'divorced': 'NA',
                'husbandId': '@I4@',
                'husbandName': 'Irwin /Trout/',
                'wifeId': '@I5@',
                'wifeName': 'Gina /Koi/',
                'children': ['@I15@']
            },
            '@F3@': {
                'id': '@F3@',
                'married': '2 JAN 1970',
                'divorced': 'NA',
                'husbandId': '@I5@',
                'husbandName': 'Irwin /Trout/',
                'wifeId': '@I6@',
                'wifeName': 'Gina /Koi/',
                'children': []
            }
        }
#        self.familiesDictNormal = {}

    def test_not_unique(self):
        self.assertEqual(
            verifier.US24_unique_families_by_spouse(
                familiesDict=self.familiesDictDup,
            ),
            False,
        )

    def test_unique(self):
        self.assertEqual(
            verifier.US24_unique_families_by_spouse(
#                familiesDict=self.familiesDictNormal,
            ),
            True,
        )

class US43ColorCodeGendersTestCases(unittest.TestCase):
    def setUp(self):
        self.individualsDict = {
            '@I1@':{
            'id': '@I1@',
            'name': 'Alice /Trout/',
            'gender': 'F',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F2@',
            'spouse': '@F1@'
            },
            '@I2@':{
            'id': '@I2@',
            'name': 'Dan /Trout/',
            'gender': 'M',
            'birthday': '2 DEC 1970',
            'age': 49,
            'alive': True,
            'death': 'NA',
            'child': '@F3@',
            'spouse': '@F1@'
            }
        }

    def test_boy(self):
        print()
        print("Boys names are blue:")
        utils.print_individual(self.individualsDict['@I2@'], ['name'])

    def test_girl(self):
        print()
        print("Girls names are pink:")
        utils.print_individual(self.individualsDict['@I1@'], ['name'])


class US25TestCases(unittest.TestCase):
    def test_unique1(self):
        self.assertTrue(verifier.US25_unique_first_name_and_birthdate(examples.exampleFamilyWithUniqueFirstNameAndBirth, examples.exampleIndividualsDict))

    def test_not_unique(self):
        self.assertFalse(verifier.US25_unique_first_name_and_birthdate(examples.exampleFamilyNotUniqueFirstNameAndBirth, examples.exampleIndividualsDict))

    def test_unique2(self):
        self.assertTrue(verifier.US25_unique_first_name_and_birthdate(examples.exampleFamilyWithUniqueFirstNameAndBirth2, examples.exampleIndividualsDict))

class US31TestCases(unittest.TestCase):
    # US31: Living and single
    def test_living_single(self):
        self.assertTrue(verifier.US31_verify_living_single(examples.exampleLivingAndSingle))

    def test_living_married(self):
        self.assertFalse(verifier.US31_verify_living_single(examples.exampleLivingAndMarried))

    def test_dead_single(self):
        self.assertFalse(verifier.US31_verify_living_single(examples.exampleDeadAndSingle))

    def test_dead_married(self):
        self.assertFalse(verifier.US31_verify_living_single(examples.exampleDeadAndMarried))
class TestMarriageCousin(unittest.TestCase):
    def test_allowed_marriage(self):
        self.assertTrue(verifier.US19_verify_no_first_cousin_marriage(examples.exampleIndividualAliveMarried))

    def test_cousin_marriage(self):
        self.assertFalse(verifier.US19_verify_no_first_cousin_marriage(examples.exampleIndividualCousinMarriage))

class AverageLifeSpanTestCase(unittest.TestCase):
    # US55: Average lifespan of dead individuals
    def test_average_arb(self):
        dead_individuals = [
            {'birthday': '10 MAR 1962',
             'death': '10 MAR 1963',
             'alive': False},
            {'birthday': '25 FEB 1998',
             'death': '25 FEB 2000',
             'alive': False},
            {'birthday': '2 DEC 1956',
             'death': '2 DEC 1959',
             'alive': False}]
        self.assertEqual(verifier.US55_get_average_lifespan(dead_individuals), 2)

    def test_average_ind(self):
        dead_individuals = [
            {'birthday': '2 DEC 1956',
             'death': '2 DEC 1959',
             'alive': False}]
        self.assertEqual(verifier.US55_get_average_lifespan(dead_individuals), 3)
        return

    def test_average_none_dead(self):
        dead_individuals = [
            {'birthday': '10 MAR 1962',
             'death': '10 MAR 1963',
             'alive': True},
            {'birthday': '25 FEB 1998',
             'death': '25 FEB 2000',
             'alive': True},
            {'birthday': '2 DEC 1956',
             'death': '2 DEC 1959',
             'alive': True}]
        self.assertEqual(verifier.US55_get_average_lifespan(dead_individuals), -1)

    def test_average_empty_list(self):
        dead_individuals = []
        self.assertEqual(verifier.US55_get_average_lifespan(dead_individuals), -1)
        return

class US26TestCase(unittest.TestCase):
    def test_consistent(self):
        individualsDict = {
            "I1": {
                "id": "I1",
                "child": "NA",
                "spouse": "F1",
            },
            "I2": {
                "id": "I2",
                "child": "NA",
                "spouse": "F1",
            },
            "I3": {
                "id": "I3",
                "child": "F1",
                "spouse": "NA",
            },
        }

        familiesDict = {
            "F1": {
                "id": "F1",
                "husbandId": "I1",
                "wifeId": "I2",
                "children": ["I3"],
            },
        }

        for _, individual in individualsDict.items():
            self.assertTrue(
                verifier.US26_corresponding_entities_individuals(
                    individual,
                    familiesDict=familiesDict,
                ),
            )

        for _, family in familiesDict.items():
            self.assertTrue(
                verifier.US26_corresponding_entities_families(
                    family,
                    individualsDict=individualsDict,
                ),
            )

    def test_incogsistent_family(self):
        individualsDict = {
            "I1": {
                "id": "I1",
                "child": "NA",
                "spouse": "F1",
            },
            "I3": {
                "id": "I3",
                "child": "F1",
                "spouse": "NA",
            },
        }

        familiesDict = {
            "F1": {
                "id": "F1",
                "husbandId": "I1",
                "wifeId": "I2",
                "children": ["I3"],
            },
        }

        for _, family in familiesDict.items():
            self.assertFalse(
                verifier.US26_corresponding_entities_families(
                    family,
                    individualsDict=individualsDict,
                ),
            )

    def test_consistent_individual(self):
        individualsDict = {
            "I1": {
                "id": "I1",
                "child": "NA",
                "spouse": "F1",
            },
            "I2": {
                "id": "I2",
                "child": "NA",
                "spouse": "F1",
            },
            "I3": {
                "id": "I3",
                "child": "F1",
                "spouse": "NA",
            },
        }

        familiesDict = {
            "F1": {
                "id": "F1",
                "husbandId": "I1",
                "wifeId": "I2",
                "children": "NA",
            },
        }

        self.assertFalse(
            verifier.US26_corresponding_entities_individuals(
                individualsDict["I3"],
                familiesDict=familiesDict,
            ),
        )

if __name__ == '__main__':
    gedcom_file = 'cs555project03.ged'
    individuals, families = parse.parse_gedcom_file_03(gedcom_file)
    verifier.initialize_verifier(individuals, families)
    unittest.main()
