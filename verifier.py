from copy import deepcopy
from datetime import date, datetime
from utils import *

individualsDict = {}
familiesDict = {}

def initialize_verifier(individuals, families):
    global individualsDict
    global familiesDict

    individualsDict = individuals
    familiesDict = families

def find_individual(individual_id):
    return individualsDict[individual_id]

def find_family(family_id):
    return familiesDict[family_id]

# User Story 01: Date is before the current date
def US01_verify_date_before_current_date(date_string):
    today = datetime_to_gedcom_date(datetime.now())
    return date_occurs_before_cond(date_string, today, date_string)

# User Story 02: Birth before marriage
def US02_verify_birth_before_marriage(individual):
    if individual['spouse'] == 'NA':
        return True

    family = find_family(individual['spouse'])
    return date_occurs_before(individual['birthday'], family['married'])

def US03_verify_birth_before_death(individual):
    return individual['alive'] or date_occurs_before(individual['birthday'], individual['death'])

def US04_verify_marriage_before_divorce(family):
    return date_occurs_before_cond(family['married'], family['divorced'], family['divorced'])

def US05_verify_marriage_before_death(family):
    wife = individualsDict[family['wifeId']]
    husband = individualsDict[family['husbandId']]
    
    marriageDate = family['married']

    wifeStatus = wife['alive'] or date_occurs_before(marriageDate, wife['death'])
    husbandStatus = husband['alive'] or date_occurs_before(marriageDate, husband['death'])

    return wifeStatus and husbandStatus

def US06_verify_divorce_before_death(family):
    husband = find_individual(family['husbandId'])
    wife = find_individual(family['wifeId'])

    wifeStatus = wife['alive'] or date_occurs_before_cond(family['divorced'], wife['death'], family['divorced'])
    husbandStatus = husband['alive'] or date_occurs_before_cond(family['divorced'], husband['death'], family['divorced'])

    return wifeStatus and husbandStatus

def US07_verify_death_before_150_years_old(individual):
    age = datetime_to_gedcom_date(datetime.now()) if individual['alive'] else individual['death']
    return dates_within(individual['birthday'], age, 150, 'years')

def US08_verify_birth_after_parents_marriage(individual):
    """
    children should be born after marriage of parents
    and not more than 9 months after divorce
    """
    if individual['child'] == 'NA':
        return True

    family = find_family(individual['child'])
    
    wedding_status = date_occurs_before(family['married'], individual['birthday'])
    divorce_status = dates_within_cond(family['divorced'], individual['birthday'], 9, 'months', family['divorced'])

    return wedding_status or divorce_status
    #print(f"ERR: Child {child_id} born before parents marriage")
    #print(f"ERR: Child {child_id} born more than 9 mo. after parent's divorce")

def US10_verify_marriage_after_14(family):
    wifeBirthday = find_individual(family['wifeId'])['birthday']
    husbandBirthday = find_individual(family['husbandId'])['birthday']

    marriageDate = family['married']

    wifeStatus = not dates_within(wifeBirthday, marriageDate, 14, 'years')
    husbandStatus = not dates_within(husbandBirthday, marriageDate, 14, 'years')

    return wifeStatus and husbandStatus

def US11_verify_no_bigamy(family):
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

def US12_verify_parents_not_too_old(family):
    valid = True

    motherAge = find_individual(family['wifeId'])['age']
    fatherAge = find_individual(family['husbandId'])['age']
    children  = family['children']

    for child in children:
        childAge = find_individual(child)['age']
        if motherAge - childAge > 60 or fatherAge - childAge > 80:
            valid = False

    return valid
    #print(f"ERR: Child {child} has too old of a parent")

def US15_verify_fewer_than_15_siblings(family):
    if len(family['children']) < 15:
        return True
    else:
        return False

def US18_verify_marriage_not_siblings(family):
    wife = find_individual(family['wifeId'])
    husband = find_individual(family['husbandId'])

    # if either don't have parent info, automatically pass
    if wife['child'] == 'NA' or husband['child'] == 'NA':
        return True

    # if both have the same parents
    return wife['child'] != husband['child']

def US21_verify_marriage_gender_roles(family):
    """Checks if a marriage is between a male and a female.

    Parameters
    ----------
    family : dict
    Returns
    -------
    bool
        True if the marriage is valid. False otherwise.
    """

    wife = find_individual(family['wifeId'])
    husband = find_individual(family['husbandId'])

    return wife['gender'] == 'F' and husband['gender'] == 'M'

# US29: List deceased individuals
def US29_verify_deceased(individual):
    return not individual['alive']

# US30: List living married individuals
def US30_verify_living_married(individual):
    return individual['alive'] and individual['spouse'] != 'NA'

# US35: List recent births
def US35_verify_birth_at_recent_30_days(individual):
    today = datetime_to_gedcom_date(datetime.now())
    return dates_within(individual['birthday'], today, 30, 'days')
    
# US36: List recent deaths
def US36_verify_death_at_recent_30_days(individual):
    today = datetime_to_gedcom_date(datetime.now())
    return (not individual['alive']) and dates_within(individual['death'], today, 30, 'days')
    #print(f"Family member {name} died on {person['death']}")

def verify():
    for id, family in familiesDict.items():
        if not US01_verify_date_before_current_date(family['married']):
            print(f"US01-ERR: Family {id} has a marriage date that is after, or equal to, the current date")
        if not US01_verify_date_before_current_date(family['divorced']):
            print(f"US01-ERR: Family {id} has a divorced date that is after, or equal to, the current date")
        if not US04_verify_marriage_before_divorce(family):
            print(f"US04-ERR: Family {id} fails marriage before divorce check")
        if not US05_verify_marriage_before_death(family):
            print(f"US05-ERR: Family {id} fails marriage before death check")
        if not US06_verify_divorce_before_death(family):
            print(f"US06-ERR: Family {id} fails divorce before death check")
        if not US10_verify_marriage_after_14(family):
            print(f"US10-ERR: Family {id} fails marriage after 14 check")
        if not US11_verify_no_bigamy(family):
            print(f"US11-ERR: Family {id} fails bigamy check")   
        if not US12_verify_parents_not_too_old(family):
            print(f"US12-ERR: Family {id} had children with parents who are too old")
        if not US15_verify_fewer_than_15_siblings(family):
            print(f"US15-ERR: Family {id} has more than 14 siblings")
        if not US18_verify_marriage_not_siblings(family):
            print(f"US18-ERR: Family {id} fails marriage between siblings check")
        if not US21_verify_marriage_gender_roles(family):
            print(f"US21-ERR: Family {id} does not pass gender roles test")
     
    for id, individual in individualsDict.items():
        if not US01_verify_date_before_current_date(individual['birthday']):
            print(f"US01-ERR: Individual {id} has a birthday that is after, or equal to, the current date")
        if not US01_verify_date_before_current_date(individual['death']):
            print(f"US01-ERR: Individual {id} has a death date that is after, or equal to, the current date")
        if not US02_verify_birth_before_marriage(individual):
            print(f"US02-ERR: Individual {id} was married before they were born")
        if not US03_verify_birth_before_death(individual):
            print(f"US03-ERR: Individual {id} was born after they died")
        if not US07_verify_death_before_150_years_old(individual):
            print(f"US07-ERR: Individual {id} is over 150 years old or lived to be over 150")
        if not US08_verify_birth_after_parents_marriage(individual):
            print(f"US08-ERR: Individual {id} was born before marriage of parents or too late after divorce")
        if US29_verify_deceased(individual):
            print(f"US29-INFO: Individual {id} is deceased")
        if US30_verify_living_married(individual):
            print(f"US30-INFO: Individual {id} is living and married")
        if US35_verify_birth_at_recent_30_days(individual):
            print(f"US35-INFO: Individual {id} was born within 30 days")
        if US36_verify_death_at_recent_30_days(individual):
            print(f"US36-INFO: Individual {id} has died within 30 days")
