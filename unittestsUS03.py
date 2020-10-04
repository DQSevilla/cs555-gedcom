import unittest
import time, datetime

import project03
import examples

class TestVerifyBirthBeforeDeath(unittest.TestCase):

    def testPersonAlive(self):
        self.assertTrue(project03.verifyBirthBeforeDeath(examples.examplePersonAlive))

    def testPersonDead(self):
        self.assertTrue(project03.verifyBirthBeforeDeath(examples.examplePersonDead))
    
    def testPersonDeadBeforeBirth(self):
        self.assertTrue(project03.verifyBirthBeforeDeath(examples.examplePersonDeadBeforeBirth))

    def testPersonSameBirthAndDeath(self):
        self.assertTrue(project03.verifyBirthBeforeDeath(examples.examplePersonSameBirthAndDeath))

    def testPersonNotBirthed(self):
        self.assertTrue(project03.verifyBirthBeforeDeath(examples.examplePersonNotBirthed))

if __name__ == '__main__':
    project03.processFile(project03.GEDCOM_FILE)
    unittest.main()