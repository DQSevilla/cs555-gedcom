import unittest
from project04 import ensureMarriageGenderRoles

class TestMarriageVerification(unittest.TestCase):

    def setUp(self):
        self.ind1 = {
            "id": "1",
            "name": "A",
            "gender": "",
            "birthday": "",
            "age": "",
            "alive": True,
            "death": "NA",
            "child": "NA",
            "spouse": "2"
        }

        self.ind2 = {
            "id": "2",
            "name": "B",
            "gender": "",
            "birthday": "",
            "age": "",
            "alive": True,
            "death": "NA",
            "child": "NA",
            "spouse": "1"
        }
    
    def test_married_normal(self):
        self.ind1["gender"] = "M"
        self.ind2["gender"] = "F"
        self.assertTrue(ensureMarriageGenderRoles(self.ind1, self.ind2))

    def test_married_normal_swapped(self):
        self.ind1["gender"] = "F"
        self.ind2["gender"] = "M"
        self.assertTrue(ensureMarriageGenderRoles(self.ind1, self.ind2))

    def test_married_both_male(self):
        self.ind1["gender"] = "M"
        self.ind2["gender"] = "M"
        self.assertFalse(ensureMarriageGenderRoles(self.ind1, self.ind2))
        
    def test_married_both_female(self):
        self.ind1["gender"] = "F"
        self.ind2["gender"] = "F"
        self.assertFalse(ensureMarriageGenderRoles(self.ind1, self.ind2))
        
    def test_married_invalid_genders(self):
        self.ind1["gender"] = "E"
        self.ind2["gender"] = "A"
        self.assertFalse(ensureMarriageGenderRoles(self.ind1, self.ind2))


if __name__ == "__main__":
    unittest.main()
