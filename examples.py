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
    'birthday': '20 SEP 2020',
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
    'death': '1 OCT 2020',
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
    'death': '1 SEP 2020',
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

exampleDateBeforeCurrentDate = '2 DEC 1970'

exampleDateAfterCurrentDate = datetime_to_gedcom_date(datetime.today() + timedelta(days=1))

exampleDateEqualCurrentDate = datetime_to_gedcom_date(datetime.now())

exampleInd1 = {
    'birthday': '2 DEC 1999'
}

exampleInd2 = {
    'birthday': '2 DEC 1999'
}

exampleInd3 = {
    'birthday': '2 DEC 1999'
}

exampleInd4 = {
    'birthday': '2 DEC 1999'
}

exampleInd5 = {
    'birthday': '2 DEC 1999'
}

exampleInd6 = {
    'birthday': '4 DEC 1999'
}

exampleInd7 = {
    'birthday': '4 DEC 1999'
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
    '@I15@': exampleInd15
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