import unittest
import examples
from project03 import verifyMarriageNotSiblings

class TestMarriageBetweenSiblingsVerification(unittest.TestCase):

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
        self.assertTrue(verifyMarriageNotSiblings(self.families['@F1@'],
                                                  self.individuals))

    def test_between_siblings(self):
        self.assertFalse(verifyMarriageNotSiblings(self.families['@F2@'],
                                                   self.individuals))

    def test_husband_parent_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.assertTrue(verifyMarriageNotSiblings(self.families['@F2@'],
                                                  self.individuals))

    def test_wife_parent_na(self):
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(verifyMarriageNotSiblings(self.families['@F2@'],
                                                  self.individuals))

    def test_both_parents_na(self):
        self.individuals['@I3@']['child'] = 'NA'
        self.individuals['@I4@']['child'] = 'NA'
        self.assertTrue(verifyMarriageNotSiblings(self.families['@F2@'],
                                                  self.individuals))

if __name__ == "__main__":
    unittest.main()
