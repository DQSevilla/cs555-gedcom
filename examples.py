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
