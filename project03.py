from prettytable import PrettyTable
from copy import deepcopy
from datetime import date, datetime
from utils import *
import time

GEDCOM_FILE = 'cs555project03.ged'
#GEDCOM_FILE = 'test.ged'
VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
              'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE',
              'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
IGNORE_TAGS = ['HEAD', 'TRLR', 'NOTE']
DATE_TAGS = ['BIRT', 'DEAT', 'DIV', 'MARR']
IND_TAGS = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
FAM_TAGS = ['HUSB', 'WIFE','CHIL', 'DIV', 'DATE']
MONTHS = {  'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC':12
}

individuals = []
families = []

individualsDict = {}
familiesDict = {}

# Custom compare function to sort by ID
def compare(s):
    currentId = s[0]
    # Strip all non-numeric characters from the ID
    numericFilter = list(filter(str.isdigit, currentId))
    numericString = "".join(numericFilter)
    return int(numericString)

def addRecord(record, type):
    if type == 'INDI':
        if record['id'] in individualsDict:
            print(f"ERR: Duplicate individual with id {record['id']}")
        individuals.append(list(record.values()))
        individualsDict[record['id']] = record
    else:
        if record['id'] in familiesDict:
            print(f"ERR: Duplicate family with id {record['id']}")
        families.append(list(record.values()))
        familiesDict[record['id']] = record

def getName(indId):
    # Search for the name of the individual with indID
    for ind in individuals:
        if ind[0] == indId:
            return ind[1]
    # Return None if the indId does not exist
    return None

def computeAge(d):
    today = date.today()
    age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
    return age

def convertDate(dateString):
    dateFields = dateString.split()
    return date(int(dateFields[2]), MONTHS[dateFields[1]], int(dateFields[0]))

def processFile(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()

    ind = {}
    fam = {}
    currentDate = ''
    for line in lines:
        line = line.replace('\n','')

        #Output Process
        tag_index = 2 if 'INDI' in line or ('FAM' in line and 'FAMS' not in line and 'FAMC' not in line) else 1
        fields = line.split(' ')
        tag = fields[tag_index]
        valid = 'Y' if tag in VALID_TAGS else 'N'
        level = fields[0]

        # Skip the current line if it contains an invalid tag
        # or
        if valid == 'N' or (level == '1' and tag == 'DATE') or (level == '2' and tag == 'NAME'):
            continue
        # Tag index of 2 represents an INDI or FAM line -> start of a new record
        elif tag_index == 2:
            if tag == 'INDI':
                # Skip if the current record is empty
                if not not ind:
                    # Add the most recent individual record to the list of individuals
                    addRecord(ind, tag)
                # Clear the previous Individual record
                ind = {
                    'id': '',
                    'name': '',
                    'gender': '',
                    'birthday': '',
                    'age': '',
                    'alive': True,
                    'death': 'NA',
                    'child': 'NA',
                    'spouse': 'NA'
                }

                ind['id'] = fields[1]
            else:
                # Skip if the current record is empty
                if not not fam:
                    # Add the most recent family record to the list of families if the record is not empty
                    addRecord(fam, tag)
                # Clear the previous Family record
                fam = {
                    'id': '',
                    'married': '',
                    'divorced': 'NA',
                    'husbandId': '',
                    'husbandName': '',
                    'wifeId': '',
                    'wifeName': '',
                    'children': []
                }
                fam['id'] = fields[1]
        # The current line correlates to the most recent family or individual record
        elif tag not in IGNORE_TAGS:
            # Signifies that next line will be a date corresponding to the current tag
            if tag in DATE_TAGS:
                currentDate = tag
            else:
                fields = fields[tag_index + 1:]
                args = ' '.join(fields)
                # Useable tags
                if tag == 'NAME': ind['name'] = args
                elif tag == 'SEX': ind['gender'] = args
                elif tag == 'DATE':
                    if currentDate == 'BIRT':
                        ind['birthday'] = args
                        # Compute age
                        day = int(fields[0])
                        month = MONTHS[fields[1]]
                        year = int(fields[2])
                        ind['age'] = computeAge(date(year, month, day))
                    elif currentDate == 'DEAT':
                        ind['death'] = args
                        ind['alive'] = False
                    elif currentDate == 'DIV': fam['divorced'] = args
                    elif currentDate == 'MARR': fam['married'] = args
                    # Clear the last date record
                    currentDate = ''
                elif tag == 'FAMC': ind['child'] = args
                elif tag == 'FAMS': ind['spouse'] = args
                elif tag == 'HUSB':
                    fam['husbandId'] = args
                    fam['husbandName'] = getName(args)
                elif tag == 'WIFE':
                    fam['wifeId'] = args
                    fam['wifeName'] = getName(args)
                elif tag == 'CHIL': fam['children'].append(args)
    addRecord(ind, "INDI")
    addRecord(fam, "FAM")
    

def gedcomDateToUnixTimestamp(date):
    dateArray = date.split(' ')
    month = MONTHS[dateArray[1]]
    day = dateArray[0]
    year = dateArray[2]
    timeString = '{0}/{1}/{2}'.format(day,month,year)
    return time.mktime(datetime.strptime(timeString, '%d/%m/%Y').timetuple())

def verifyMarriageBeforeDivorce(family):
    return date_occurs_before_cond(family['married'], family['divorced'], family['divorced'])

def verifyMarriageBeforeDeath(family):
    wife = individualsDict[family['wifeId']]
    husband = individualsDict[family['husbandId']]
    
    marriageDate = family['married']

    wifeStatus = wife['alive'] or date_occurs_before(marriageDate, wife['death'])
    husbandStatus = husband['alive'] or date_occurs_before(marriageDate, husband['death'])

    return wifeStatus and husbandStatus

def verifyMarriageNotSiblings(family, individuals):
    wife = individuals[family['wifeId']]
    husband = individuals[family['husbandId']]

    # if either don't have parent info, automatically pass
    if wife['child'] == 'NA' or husband['child'] == 'NA':
        return True

    # if both have the same parents
    if wife['child'] == husband['child']:
        return False

    return True

def ensureMarriageGenderRoles(family, individuals):
    """Checks if a marriage is between a male and a female.

    Parameters
    ----------
    family : dict
    individuals: dict

    Returns
    -------
    bool
        True if the marriage is valid. False otherwise.
    """

    wife = individuals[family['wifeId']]
    husband = individuals[family['husbandId']]

    if wife['gender'] != 'F' or husband['gender'] != 'M':
        return False

    return True

def verifyBirthBeforeDeath(person):
    #Get IDs of the individual in question parties in the couple
    individual = individualsDict[person['id']]

    #Get the birth date
    personBirthDate = gedcomDateToUnixTimestamp(individual['birthday'])

    #Check if they are dead, and if they are, if they died before their birth
    if not individual['alive']:
        personDeathDate = gedcomDateToUnixTimestamp(individual['death'])
        if personDeathDate < personBirthDate:
            return False
    return True


def verifyDivorceBeforeDeath(family):
    if family['divorced'] == 'NA':
        return True

    divorceTime = gedcomDateToUnixTimestamp(family['divorced'])

    husband = individualsDict[family['husbandId']]
    wife = individualsDict[family['wifeId']]

    if not husband['alive']:
        deathDate = gedcomDateToUnixTimestamp(husband['death'])
        if deathDate < divorceTime:
            print(f"ERR husband in family {family['id']} died before divorce")
            return False

    if not wife['alive']:
        deathDate = gedcomDateToUnixTimestamp(wife['death'])
        if deathDate < divorceTime:
            print(f"ERR wife in family {family['id']} died before divorce")
            return False

    return True

def verifyDeathBefore150YearsOld(person):
    bday_unix = gedcomDateToUnixTimestamp(person['birthday'])
    if person['death'] == 'NA':
        age = time.time() - bday_unix
    else:
        death_unix = gedcomDateToUnixTimestamp(person['death'])
        age = death_unix - bday_unix
    years_in_seconds = 150 * 365 * 24 * 60 * 60
    return age <= years_in_seconds

# User Story 01: Date is before the current date
def verifyDateBeforeCurrentDate(dateString):
    if dateString == 'NA':
        return True

    compareDate = convertDate(dateString)
    today = date.today()
    return compareDate < today

# User Story 02: Birth before marriage
def verifyBirthBeforeMarriage(person):
    spouse = person['spouse']
    # We will consider an unmarried individual to always have a marriage date before their birth date
    if spouse == 'NA':
        return True
    # Individuals should not have a birthday greater than or equal to their marriage date
    birthFields = person['birthday'].split()
    birthDay = date(int(birthFields[2]), MONTHS[birthFields[1]], int(birthFields[0]))

    marriedFields = familiesDict[spouse]['married'].split()
    marriedDate = date(int(marriedFields[2]), MONTHS[marriedFields[1]], int(marriedFields[0]))
    return birthDay < marriedDate

# US35: List recent births
def verifyBirthAtRecent30Days(person):
    currentDateTimestamp = time.time();
    name = person['name']
    birthdayStamp = gedcomDateToUnixTimestamp(person['birthday']);
    # If the date of birth is within 30 days
    if currentDateTimestamp - birthdayStamp < 2592000:
        print(f"Family member {name} was born on {person['birthday']}")
        return True
    else:
        return False

# US36: List recent deaths
def verifyDeathAtRecent30Days(person):
    currentDateTimestamp = time.time();
    if not person['alive']:
        name = person['name']
        deathDateStamp = gedcomDateToUnixTimestamp(person['death']);
        # If the date of death is within 30 days
        if currentDateTimestamp - deathDateStamp < 2592000:
            print(f"Family member {name} was dead on {person['death']}")
            return True
        else:
            return False
    else:
        return False

def verifyBirthAfterParentsMarriage(family):
    """
    children should be born after marriage of parents
    and not more than 9 months after divorce
    """
    errors = False
    marriage_date = gedcomDateToUnixTimestamp(family['married'])
    for child_id in family['children']:
        child = individualsDict[child_id]
        birthday = gedcomDateToUnixTimestamp(child['birthday'])
        if birthday < marriage_date:
            errors = True
            print(f"ERR: Child {child_id} born before parents marriage")
        if family['divorced'] != 'NA':
            divorce_date = gedcomDateToUnixTimestamp(family['divorced'])
            if birthday > (divorce_date + 2764800):  # 9 mo. after divorce
                errors = True
                print(f"ERR: Child {child_id} born more than 9 mo. after parent's divorce")
    return errors

def verifyParentsNotTooOld(family):
    errors = False

    motherAge = individualsDict[family['wifeId']]['age']
    fatherAge = individualsDict[family['husbandId']]['age']
    children  = family['children']

    for child in children:
        childAge = individualsDict[child]['age']
        if motherAge - childAge > 60 or fatherAge - childAge > 80:
            print(f"ERR: Child {child} has too old of a parent")
            errors = True

    return not errors

def verifyNoBigamy(family):
    #retrieve ID for husband and wife
    husbandID = family['husbandId']
    wifeID = family['wifeId']
    #make a modified family dictionary without family in question
    modifiedDict = deepcopy(familiesDict)
    modifiedDict.pop(family['id'])

    #check every other family
    for fam in modifiedDict.values():
        #if another family's husband ID is identical
        if husbandID == fam['husbandId']:
            return False
        #if another family's wife ID is identical
        if wifeID == fam['wifeId']:
            return False
            
    #unique ID for both husband and wife in family
    return True

def verifyMarriageAfter14(family):
    #get individuals by ID
    wife = individualsDict[family['wifeId']]
    husband = individualsDict[family['husbandId']]

    #get their marriage date
    marriageDate = gedcomDateToUnixTimestamp(family['married'])

    #14 years in unix = 441849600
    years14Unix = 441849600
    wifeBirth = gedcomDateToUnixTimestamp(wife['birthday'])
    husBirth = gedcomDateToUnixTimestamp(husband['birthday'])
    #if both wife and husband's marriage date minus their birthdays are both over 14 years unix
    if (marriageDate - husBirth > years14Unix and marriageDate - wifeBirth > years14Unix):
        return True
    else:
        return False

def main():
    processFile(GEDCOM_FILE)
    # Table of Individuals
    individualsTable = PrettyTable()
    individualsTable.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
    # Sort the list of individuals by ID
    individuals.sort(key=compare)
    for ind in individuals:
        individualsTable.add_row(ind)

    # Table of Families
    familiesTable = PrettyTable()
    familiesTable.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
    # Sort the list of families by ID
    individuals.sort(key=compare)
    for family in families:
        familiesTable.add_row(family)

    print(individualsTable)
    print(familiesTable)

    for family in familiesDict:
        if not verifyMarriageBeforeDivorce(familiesDict[family]):
            print('Family {0} fails marriage before divorce check'.format(family))
        if not verifyMarriageBeforeDeath(familiesDict[family]):
            print('Family {0} fails marriage before death check'.format(family))
        if not verifyNoBigamy(familiesDict[family]):
            print('Family {0} fails bigamy check'.format(family))

        if not verifyDateBeforeCurrentDate(familiesDict[family]['married']):
            print(f"Family {family} has a marriage date that is after, or equal to, the current date")
        if not verifyDateBeforeCurrentDate(familiesDict[family]['divorced']):
            print(f"Family {family} has a divorced date that is after, or equal to, the current date")
        verifyBirthAfterParentsMarriage(familiesDict[family])

        if not ensureMarriageGenderRoles(familiesDict[family], individualsDict):
            print('Family {0} fails proper gender role check'.format(family))

        if not verifyMarriageNotSiblings(familiesDict[family], individualsDict):
            print('Family {0} fails marriage between siblings check'.format(family))

        verifyParentsNotTooOld(familiesDict[family])
        if not verifyMarriageAfter14(familiesDict[family]):
            print('Family {0} fails marriage after 14 check'.format(family))

        verifyDivorceBeforeDeath(familiesDict[family])

    for id, individual in individualsDict.items():
        if not verifyDeathBefore150YearsOld(individual):
            print(f"ERR: Individual {id} is over 150 years old")
        if not verifyBirthBeforeDeath(individual):
            print(f"ERR: Individual {id} was born after they died")
        if not verifyDateBeforeCurrentDate(individual['birthday']):
            print(f"ERR: Individual {id} has a birthday that is after, or equal to, the current date")
        if not verifyDateBeforeCurrentDate(individual['death']):
            print(f"ERR: Individual {id} has a death date that is after, or equal to, the current date")
        if not verifyBirthBeforeMarriage(individual):
            print(f"ERR: Individual {id} has a birthday after their marriage date")
        verifyBirthAtRecent30Days(individual)
        verifyDeathAtRecent30Days(individual)

if __name__ == '__main__':
    main()
