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
    'age': 154,
    'alive': False,
    'death': '30 NOV 2119',
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

exampleBirthdayNA = {
    'id': '@I1@',
    'name': 'Alice /Trout/',
    'gender': 'F',
    'birthday': 'NA',
    'age': 49,
    'alive': True,
    'death': 'NA',
    'child': '@F2@',
    'spouse': '@F1@'
}