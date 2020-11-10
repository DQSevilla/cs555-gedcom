from utils import datetime_to_gedcom_date
from datetime import datetime
from datetime import timedelta

examplePersonAlive = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

examplePersonAliveOnePointFive = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'M',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

examplePersonAlive2 = {
    'id': '@I2@',
    'name': 'George /Salmon/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F5@',
    'spouse': '@F1@'
}

examplePersonDead = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '31 DEC 1949',
    'age': 70,
    'alive': False,
    'death': '14 FEB 2015',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonDead150 = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '1 JAN 1970',
    'age': 150,
    'alive': False,
    'death': '26 NOV 2119',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonAliveOver150 = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '1 JAN 1000',
    'age': 151,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonDeadOver150 = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '1 JAN 1970',
    'age': 249,
    'alive': False,
    'death': '30 NOV 2219',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonDeadBeforeBirth = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '31 DEC 1949',
    'age': 70,
    'alive': False,
    'death': '14 FEB 1940',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonNotBirthed = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': 'NA',
    'age': 70,
    'alive': False,
    'death': 'NA',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonSameBirthAndDeath = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '14 FEB 1940',
    'age': 70,
    'alive': True,
    'death': '14 FEB 1940',
    'child': 'NA',
    'spouse': '@F2@'
}
examplePersonRecentBirth = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': datetime_to_gedcom_date(datetime.now()),
    'age': 0,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonRecentDeath = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '14 FEB 1940',
    'age': 70,
    'alive': False,
    'death': datetime_to_gedcom_date(datetime.now()),
    'child': 'NA',
    'spouse': '@F2@'
}

examplePersonNotRecentDeath = {
    'id': '@I5@',
    'name': 'Gina /Koi/',
    'gender': 'F',
    'birthday': '14 FEB 1940',
    'age': 70,
    'alive': False,
    'death': '1 SEP 1941',
    'child': 'NA',
    'spouse': '@F2@'
}

exampleFamilyTogether = {
    'id': '@F1@',
    'married': '14 MAY 1994',
    'divorced': 'NA',
    'husbandId': '@I2@',
    'husbandName': 'George /Salmon/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I3@', '@I16@']
}

exampleFamilyDivorced = {
    'id': '@F5@',
    'married': '31 JUL 2003',
    'divorced': '31 JUL 2005',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I13@',
    'wifeName': 'Trusha /Squid/',
    'children': ['@I12@']
}

exampleImproperFamilyDivorced = {
    'id': '@F5@',
    'married': '31 JUL 2003',
    'divorced': '31 JUL 2002',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I13@',
    'wifeName': 'Trusha /Squid/',
    'children': ['@I12@']
}

exampleFamilyWithWidow = {
    'id': '@F2@',
    'married': '2 JAN 1970',
    'divorced': 'NA',
    'husbandId': '@I4@',
    'husbandName': 'Irwin /Trout/',
    'wifeId': '@I5@',
    'wifeName': 'Gina /Koi/',
    'children': ['@I1@', '@I6@', '@I8@', '@I10@']
}

exampleImproperFamilyWithWidow = {
    'id': '@F2@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I4@',
    'husbandName': 'Irwin /Trout/',
    'wifeId': '@I5@',
    'wifeName': 'Gina /Koi/',
    'children': ['@I1@', '@I6@', '@I8@', '@I10@']
}


exampleFamilyGay = {
    'id': '@F1@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I2@',
    'husbandName': 'James /Boucher/',
    'wifeId': '@I1@',
    'wifeName': 'Asad /Kahn/',
    'children': []
}

exampleFamilyLesbian = {
    'id': '@F2@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I4@',
    'husbandName': 'Paula /Lloyd/',
    'wifeId': '@I3@',
    'wifeName': 'Abigail /Garcia/',
    'children': []
}

exampleFamilyBothGendersIncorrect = {
    'id': '@F3@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I3@',
    'husbandName': 'Abigail /Garcia/',
    'wifeId': '@I2@',
    'wifeName': 'James /Boucher/',
    'children': []
}

exampleFamilyInvalidGenders = {
    'id': '@F4@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I5@',
    'husbandName': 'e /e/',
    'wifeId': '@I5@',
    'wifeName': 'e /e/',
    'children': []
}

exampleFamilyCorrect = {
    'id': '@F5@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I2@',
    'husbandName': 'James /Boucher/',
    'wifeId': '@I3@',
    'wifeName': 'Abigail /Garcia/',
    'children': []
}

exampleWifeIncorrectGender = {
    'id': '@I1@',
    'name': 'Asad /Kahn/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleHusbandCorrectGender = {
    'id': '@I2@',
    'name': 'James /Boucher/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleWifeCorrectGender = {
    'id': '@I3@',
    'name': 'Abigail /Garcia/',
    'gender': 'F',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleHusbandIncorrectGender = {
    'id': '@I4@',
    'name': 'Paula /Lloyd/',
    'gender': 'F',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleIndividualInvalidGender = {
    'id': '@I5@',
    'name': 'e /e/',
    'gender': '-',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleIndividualAliveUnmarried = {
    'id': '@I1@',
    'name': 'e /e/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleIndividualAliveMarried = {
    'id': '@I1@',
    'name': 'e /e/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': True,
    'death': 'NA',
    'child': 'NA',
    'spouse': '@I2@'
}

exampleIndividualDeadUnmarried = {
    'id': '@I1@',
    'name': 'e /e/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': False,
    'death': 'NA',
    'child': 'NA',
    'spouse': 'NA'
}

exampleIndividualDeadMarried = {
    'id': '@I1@',
    'name': 'e /e/',
    'gender': 'M',
    'birthday': '2 DEC 1983',
    'age': 36,
    'alive': False,
    'death': 'NA',
    'child': 'NA',
    'spouse': '@I2@'
}

exampleFamilyBetweenSiblings = {
    'id': '@F1@',
    'married': '14 MAY 1994',
    'divorced': 'NA',
    'husbandId': '@I3@',
    'husbandName': 'Anthony /Gabario/',
    'wifeId': '@I4@',
    'wifeName': 'Serafina /Russo/',
    'children': []
}

examplePersonSameParent1 = {
    'id': '@I3@',
    'name': 'Anthony /Gabario/',
    'gender': 'M',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F1@'
}

examplePersonSameParent2 = {
    'id': '@I4@',
    'name': 'Serafina /Russo/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F1@'
}

examplePersonSameBirthday1 = {
    'id': '@I1@',
    'name': 'Serafina /Russo/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F1@'    
}

examplePersonSameBirthday2 = {
    'id': '@I2@',
    'name': 'Adam /Jeffries/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F2@'    
}

examplePersonDifferentBirthday1 = {
    'id': '@I1@',
    'name': 'Serafina /Russo/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F1@'    
}

examplePersonDifferentBirthday2 = {
    'id': '@I2@',
    'name': 'Adam /Jeffries/',
    'gender': 'F',
    'birthday': '20 MAR 1971',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F3@',
    'spouse': '@F2@'    
}

exampleFamilyWithTooYoungKid = {
    'id': '@F2@',
    'married': '2 JAN 1970',
    'divorced': 'NA',
    'husbandId': '@I4@',
    'husbandName': 'Irwin /Trout/',
    'wifeId': '@I5@',
    'wifeName': 'Gina /Koi/',
    'children': ['@I15@']
}

exampleBirthdayBeforeMarriage = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

exampleBirthdayAfterMarriage = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '2 DEC 2020',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

exampleBirthdayEqualMarriage = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '14 MAY 1994',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

exampleOrphan = {
    'id': '@I71@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '14 MAY 2007',
    'age': 13,
    'alive': True,
    'death': 'NA',
    'child': '@F72@',
    'spouse': '@F71@'
}

exampleFatherOfOrphan = {
    'id': '@I72@',
    'name': 'John /Trout/',
    'gender': 'M',
    'birthday': '14 MAY 1954',
    'age': 66,
    'alive': False,
    'death': 'NA',
    'child': '@F73@',
    'spouse': '@F72@'
}

exampleMatherOfOrphan = {
    'id': '@I73@',
    'name': 'Amy /Trout/',
    'gender': 'F',
    'birthday': '14 MAY 1989',
    'age': 31,
    'alive': False,
    'death': 'NA',
    'child': '@F74@',
    'spouse': '@F72@'
}

exampleOrphanFamily = {
    'id': '@F72@',
    'married': '2 JAN 2005',
    'divorced': 'NA',
    'husbandId': '@I72@',
    'husbandName': 'John /Goldfish/',
    'wifeId': '@I73@',
    'wifeName': 'Amy /Trout/',
    'children': ['@I71@']
}

exampleMarriage14YearsAfterBoth = {
    'id': '@F1@',
    'married': '2 JAN 2020',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I13@',
    'wifeName': 'Alice /Trout/', #1970
    'children': []
}

exampleMarriageHusbandOver14Years = {
    'id': '@F1@',
    'married': '2 JAN 2010',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I14@',
    'wifeName': 'Anna /Goldfish/', #2000
    'children': []
}

exampleMarriageWifeOver14Years = {
    'id': '@F3@',
    'married': '2 JAN 2000',
    'divorced': 'NA',
    'husbandId': '@I3@',
    'husbandName': 'John /Salmon/', #1997
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': []
}

exampleMarriage14YearsBeforeBoth = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': []
}

exampleFamilyOver15Siblings = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I1@', '@I2@', '@I3@', '@I4@', '@I5@', '@I6@', '@I7@', '@I8@', '@I9@', '@I10@', '@I11@', '@I12@', '@I13@', '@I14@', '@I15@', '@I16@']
}

exampleBornAfterDeathParents = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '15 FEB 2015',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}

exampleBornBeforeDeathParents = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '15 FEB 2015',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F1@',
    'spouse': '@F1@'
}

exampleBornAfter9MonthsFather = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '21 NOV 2001',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F4@',
    'spouse': '@F1@'
}

exampleBornBefore9MonthsFather = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '21 NOV 2000',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F4@',
    'spouse': '@F1@'
}

exampleFamilyOneChild = {
    'id': '@F3@',
    'married': '2 JAN 2000',
    'divorced': 'NA',
    'husbandId': '@I3@',
    'husbandName': 'John /Salmon/', #1997
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@']
}


exampleTwinFamily = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I17@', '@I15@']
}

exampleSpacedFamily = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I1@', '@I12@', '@I16@', '@I18@']
}

exampleNonSpacedFamily = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I13@', '@I14@', '@I17@', '@I15@']
}

exampleIndividualCousinMarriage = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '21 NOV 2000',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F4@'
}

exampleDateBeforeCurrentDate = '2 DEC 1970'

exampleDateAfterCurrentDate = datetime_to_gedcom_date(datetime.today() + timedelta(days=1))

exampleDateEqualCurrentDate = datetime_to_gedcom_date(datetime.now())

exampleInd1 = {
    'birthday': '2 DEC 1999',
    'gender': 'F',
    'name': "Alice /Trout/"
}

exampleInd2 = {
    'birthday': '2 DEC 1999',
    'gender': 'M',
    'name': "Simon /Gao/"
}

exampleInd3 = {
    'birthday': '2 DEC 1999',
    'gender': 'M',
    'name': 'John /Doe/'
}

exampleInd4 = {
    'birthday': '2 DEC 1999',
    'gender': 'M',
    'name': 'Sean /Gao/'
}

exampleInd5 = {
    'birthday': '2 DEC 1999',
    'gender': 'M',
    'name': 'Xian /Gao/'
}

exampleInd6 = {
    'birthday': '4 DEC 1999',
    'gender': 'F',
    'name': 'Michelle /Gao/'
}

exampleInd7 = {
    'birthday': '4 DEC 1999',
    'gender': 'F',
    'name': 'Jane /Gao/'
}

exampleInd8 = {
    'birthday': '4 DEC 1999'
}

exampleInd9 = {
    'birthday': '4 DEC 1999'
}

exampleInd10 = {
    'birthday': '4 DEC 1999'
}

exampleInd11 = {
    'birthday': '4 DEC 1999'
}

exampleInd12 = {
    'birthday': '25 DEC 1998'
}

exampleInd13 = {
    'birthday': '4 JUN 1999'
}

exampleInd14 = {
    'birthday': '12 AUG 1999'
}

exampleInd15 = {
    'birthday': ' 30 JAN 2000'
}

exampleInd16 = {
    'birthday': '2 MARCH 1970',
    'gender': 'M',
    'name': 'Jeff /Gao/'
}

exampleInd17 = {
    'birthday': '29 JAN 2000'
}

exampleInd18 = {
    'birthday': '20 MAY 1980'
}

exampleInd19 = {
    'birthday': '2 MARCH 1970',
    'gender': 'M',
    'name': 'Simp /Gao/'
}

exampleInd20 = {
    'birthday': '2 MARCH 1970',
    'gender': 'M',
    'name': 'Simp /Gao/'
}

exampleInd21 = {
    'birthday': '4 MARCH 1970',
    'gender': 'M',
    'name': 'Simp /Gao/'
}

exampleIndividualsDict = {
    '@I1@': exampleInd1,
    '@I2@': exampleInd2,
    '@I3@': exampleInd3,
    '@I4@': exampleInd4,
    '@I5@': exampleInd5,
    '@I6@': exampleInd6,
    '@I7@': exampleInd7,
    '@I8@': exampleInd8,
    '@I9@': exampleInd9,
    '@I10@': exampleInd10,
    '@I11@': exampleInd11,
    '@I12@': exampleInd12,
    '@I13@': exampleInd13,
    '@I14@': exampleInd14,
    '@I15@': exampleInd15,
    '@I16@': exampleInd16,
    '@I17@': exampleInd17,
    '@I18@': exampleInd18,
    '@I19@': exampleInd19,
    '@I20@': exampleInd20,
    '@I21@': exampleInd21
}

exampleFamilyChildrenBirthLessThan5 = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I1@', '@I5@', '@I8@', '@I12@', '@I15@']
}

exampleFamilyChildrenBirthEqual5 = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I1@', '@I2@', '@I3@', '@I4@', '@I5@', '@I6@', '@I7@', '@I8@', '@I9@', '@I10@']
}

exampleFamilyChildrenBirthGreaterThan5 = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I6@', '@I7@', '@I8@', '@I9@', '@I10@', '@I11@']
}

exampleFamilyMalesWithSameLastName = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I4@', '@I5@', '@I6@', '@I7@']
}

exampleFamilyMalesWithoutSameLastName = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I3@', '@I4@', '@I5@', '@I6@', '@I7@']
}

exampleFamilyMalesWithSameLastNameButDifferentFemale = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I1@', '@I2@', '@I4@', '@I5@', '@I6@', '@I7@']
}

exampleIncomingAnniversary = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '21 NOV 2000',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F4@',
    'spouse': '@F1@'
}

exampleFarAnniversary = {
    'id': '@I2@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': '21 NOV 2000',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F4@',
    'spouse': '@F2@'
}


exampleFamilyAnni = {
    'id': '@F1@',
    'married': '29 Nov 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I1@', '@I5@', '@I8@', '@I12@', '@I15@']
}

exampleFamilyNoAnni = {
    'id': '@F2@',
    'married': '21 Jun 1975',
    'divorced': 'NA',
    'husbandId': '@I7@',
    'husbandName': 'Noah /Goldfish/',
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/',
    'children': ['@I1@', '@I5@', '@I8@', '@I12@', '@I15@']
}

exampleAnniversaryDict = {
    '@F1@' : exampleFamilyAnni,
    '@F2@' : exampleFamilyNoAnni
}

exampleFamilyWithUniqueFirstNameAndBirth = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I4@', '@I5@', '@I6@', '@I7@', '@I19@']
}

exampleSiblingOrdering = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I4@', '@I5@', '@I6@', '@I7@', '@I19@', '@I20@']
}

exampleFamilyNotUniqueFirstNameAndBirth = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I4@', '@I5@', '@I6@', '@I7@', '@I19@', '@I20@']
}

exampleFamilyWithUniqueFirstNameAndBirth2 = {
    'id': '@F4@',
    'married': '2 JAN 1975',
    'divorced': 'NA',
    'husbandId': '@I16@',
    'husbandName': 'Jeff /Gao/', #1971
    'wifeId': '@I1@',
    'wifeName': 'Alice /Trout/', #1970
    'children': ['@I2@', '@I4@', '@I5@', '@I6@', '@I7@', '@I19@', '@I21@']
}

exampleLivingAndSingle = {
    'id': '@I30@',
    'name': 'Nam /So-dan/',
    'gender': 'M',
    'birthday': '7 MAY 1995 ',
    'age': 24,
    'alive': True,
    'death': 'NA',
    'child': '@F73@',
    'spouse': 'NA'
}

exampleLivingAndMarried = {
    'id': '@I31@',
    'name': 'Han /Jipyeong/',
    'gender': 'M',
    'birthday': '7 MAY 1990',
    'age': 29,
    'alive': True,
    'death': 'NA',
    'child': '@F73@',
    'spouse': '@F72@'
}

exampleDeadAndSingle = {
    'id': '@I31@',
    'name': 'John /Jipyeong/',
    'gender': 'M',
    'birthday': '7 MAY 1990',
    'age': 29,
    'alive': False,
    'death': 'NA',
    'child': '@F73@',
    'spouse': 'NA'
}

exampleDeadAndMarried = {
    'id': '@I3@',
    'name': 'George /Salmon/',
    'gender': 'F',
    'birthday': '2 DEC 1970',
    'age': 49,
    'alive': False,
    'death': 'NA',
    'child': '@F5@',
    'spouse': '@F5'
}