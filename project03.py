from prettytable import PrettyTable
from datetime import date, datetime
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
        individuals.append(list(record.values()))
        individualsDict[record['id']] = record
    else:
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
    #Check if they're divorced at all
    if not family['divorced'] == 'NA':
        divorcedDate = gedcomDateToUnixTimestamp(family['divorced'])
        marriageDate = gedcomDateToUnixTimestamp(family['married'])

        #Check that the Unix timestamp of their divorce is after the one of their marriage
        return divorcedDate > marriageDate
    #If they're not, we're done
    else:
        return True

def verifyMarriageBeforeDeath(family):
    #Get IDs of both parties in the couple
    wife = individualsDict[family['wifeId']]
    husband = individualsDict[family['husbandId']]

    #Get the marriage date
    marriageDate = gedcomDateToUnixTimestamp(family['married'])

    #Check if they are dead, and if they are, if they died before wedding
    if not wife['alive']:
        wifeDeathDate = gedcomDateToUnixTimestamp(wife['death'])
        if wifeDeathDate < marriageDate:
            return False
    if not husband['alive']:
        husbandDeathDate = gedcomDateToUnixTimestamp(husband['death'])
        if husbandDeathDate < marriageDate:
            return False

    #If neither failed, we passed, return true
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
            # TODO: Noah: Fix this definition
            pass

def verifyDivorceBeforeDeath(person):
    #Get IDs of the individual in question parties in the couple
    individual = individualsDict[person]

    #If they have never been divorced, everything is okay
    if not person['divorced']:
        return True

    #Get the birth date
    personDivorceDate = gedcomDateToUnixTimestamp(person['divorced'])

    #Check if they are dead, and if they are, if they died before their birth
    if not person['alive']:
        personDeathDate = gedcomDateToUnixTimestamp(person['death'])
        if personDeathDate < personDivorceDate:
            return False

    #If neither failed, we passed, return true
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

def verifyBirthAfterParentsMarriage(family):
    """
    children should be born after marriage of parents
    and not more than 9 months after divorce
    """
    # get marriage date
    # if children, for all children, get birth date and check. print.
    marriage_date = gedcomDateToUnixTimestamp(family['married'])
    for child_id in family['children']:
        child = individualsDict[child_id]
        birthday = gedcomDateToUnixTimestamp(child['birthday'])
        if birthday < marriage_date:
            print(f"ERR: Child {child_id} born before parents marriage")
        if family['divorced'] != 'NA':
            divorce_date = gedcomDateToUnixTimestamp(family['divorced'])
            if birthday > (divorce_date + 2764800):  # 9 mo. after divorce
                print(f"ERR: Child {child_id} born more than 9 mo. after parent's divorce")

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
        verifyBirthAfterParentsMarriage(familiesDict[family])

    for _, individual in individualsDict.items():
        if not verifyDeathBefore150YearsOld(individual):
            print(f"ERR: Individual {id} is over 150 years old")

if __name__ == '__main__':
    main()
