import unittest
import examples
from project03 import ensureMarriageGenderRoles

class TestMarriageGendersVerification(unittest.TestCase):

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
        self.assertFalse(ensureMarriageGenderRoles(
            TestMarriageGendersVerification.families['@F1@'],
            TestMarriageGendersVerification.individuals))

    def test_married_both_female(self):
        self.assertFalse(ensureMarriageGenderRoles(
            TestMarriageGendersVerification.families['@F2@'],
            TestMarriageGendersVerification.individuals))

    def test_married_male_female_incorrect(self):
        self.assertFalse(ensureMarriageGenderRoles(
            TestMarriageGendersVerification.families['@F3@'],
            TestMarriageGendersVerification.individuals))

    def test_married_male_famele_correct(self):
        self.assertTrue(ensureMarriageGenderRoles(
            TestMarriageGendersVerification.families['@F4@'],
            TestMarriageGendersVerification.individuals))

    def test_married_invalid_genders(self):
        self.assertFalse(ensureMarriageGenderRoles(
            TestMarriageGendersVerification.families['@F5@'],
            TestMarriageGendersVerification.individuals))

if __name__ == "__main__":
    unittest.main()
