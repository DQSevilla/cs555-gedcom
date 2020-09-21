from prettytable import PrettyTable
from datetime import date

GEDCOM_FILE = 'cs555project01.ged'
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

# Custom compare function to sort by ID
def compare(s):
    currentId = s[0]
    # Strip all non-numeric characters from the ID
    numericFilter = list(filter(str.isdigit, currentId))
    numericString = "".join(numericFilter)
    return int(numericString)

def addRecord(record, type):
    #print(record)
    if type == 'INDI':
        individuals.append(list(record.values()))
    else:
        families.append(list(record.values()))

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

if __name__ == '__main__':
    main()
