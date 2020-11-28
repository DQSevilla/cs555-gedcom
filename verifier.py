from copy import deepcopy
from datetime import date, datetime
from utils import *

from collections import defaultdict

individualsDict = {}
familiesDict = {}

def initialize_verifier(individuals, families):
    global individualsDict
    global familiesDict

    individualsDict = individuals
    familiesDict = families

def find_individual(individual_id, defaultdict = None):
    return defaultdict[individual_id] if defaultdict else individualsDict[individual_id]

def find_family(family_id, defaultdict = None):
    return defaultdict[family_id] if defaultdict else familiesDict[family_id]

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

def US09_verify_birth_before_parents_death(individual):
    if individual['child'] == 'NA':
        return True

    birthday = individual['birthday']
    family = find_family(individual['child'])
    mother = find_individual(family['wifeId'])
    father = find_individual(family['husbandId'])

    mother_status = date_occurs_before_cond(birthday, mother['death'], mother['death'])
    father_status = date_occurs_before_cond(birthday, father['death'], father['death']) or dates_within(birthday, father['death'], 9, 'months')

    return mother_status and father_status

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

def US13_verify_sibling_spacing(family, local_inds = None):
    #if there is only child in the family or none, return True
    if len(family['children']) < 2:
        return True
    if local_inds == None:
        local_inds = individualsDict
    for child1 in family['children']:
        for child2 in family['children']:
            #if we're checking the same child, skip
            if child1 == child2:
                continue
            #first check if they are twins
            if dates_within(local_inds[child1]['birthday'], local_inds[child2]['birthday'], 1, 'days'):
                continue
            #then if the two children have birthday's within 8 months of each other, return False
            if dates_within(local_inds[child1]['birthday'], local_inds[child2]['birthday'], 8, 'months'):
                return False
    return True
    
def US14_verify_multiple_births(family, local_inds=None):
    # Check if there are more than 5 siblings birthed on the same day for each family
    birthdays = defaultdict(int)
    if local_inds == None:
        local_inds = individualsDict
    # Initialize the dictionary of birthdays in the family
    for ind_id in family['children']:
        ind_birthday = local_inds[ind_id]['birthday']
        birthdays[ind_birthday] += 1

    for birthday in birthdays:
        if birthdays[birthday] > 5:
            return False
    return True


def US15_verify_fewer_than_15_siblings(family):
    return len(family['children']) < 15

def US16_verify_male_last_names(family, local_inds=None):
    if local_inds == None: local_inds = individualsDict
    family_last_name = family['husbandName'].split('/')[1]
    for child_id in family['children']:
        current_child = local_inds[child_id]
        if current_child['gender'] == 'M':
            child_last_name = current_child['name'].split('/')[1]
            if family_last_name != child_last_name: return False
    return True

def US17_verify_no_marriage_to_descendants(person, individualsDict = individualsDict, familiesDict = familiesDict):
    #get individuals id
    individual = person
    if individual['spouse'] == 'NA':
        return True

    personSpouse = find_family(individual['spouse'], defaultdict = familiesDict)

    #get children and make sure they are not a spouse
    personChildren = personSpouse['children']
    personDecendants = []
    while personChildren != []:
        personDecendants.append(personChildren[0])
        kidFamily = find_individual(personChildren[0], defaultdict = individualsDict)['spouse']
        if kidFamily != 'NA':
            personChildren = personChildren + find_family(kidFamily, defaultdict = familiesDict)['children']
        personChildren = personChildren[1:]
        if personSpouse['wifeId'] in personDecendants or personSpouse['husbandId'] in personDecendants:
            return False

    return True

def US18_verify_marriage_not_siblings(family):
    wife = find_individual(family['wifeId'])
    husband = find_individual(family['husbandId'])

    # if either don't have parent info, automatically pass
    if wife['child'] == 'NA' or husband['child'] == 'NA':
        return True

    # if both have the same parents
    return wife['child'] != husband['child']

def US19_verify_no_first_cousin_marriage(individual):
    spouse = individual['spouse']
    parents = individual['child']
    if spouse == 'NA' or parents == 'NA':
        return True
    spouse = find_family(spouse)
    family = find_family(parents)

    #Get their cousins and make sure that the spouse is not in there
    individual_id = individual['id']
    children = family['children']

    #This is never true in a valid family but could be somehow in an invalid gedcom file
    if children == []:
        return True

    children.remove(individual_id)
    wife_id = spouse['wifeId']
    husband_id = spouse['husbandId']

    return not (wife_id in children or husband_id in children)

#aunts and uncles should not marry their neices and nephews
def US20_verify_aunts_and_uncles(person, individualsDict = individualsDict, familiesDict = familiesDict):
    #Get id of Aunt or Uncle
    individual = person
    if person['spouse'] == 'NA':
        return True

    if person['child'] == 'NA':
        return True

    personSiblings = find_family(person['child'], defaultdict = familiesDict)['children']

    if personSiblings == []:
        return True

    if individual['id'] in personSiblings:
        personSiblings.remove(individual['id'])
    niecesAndNephews = []

    for sibling in personSiblings:
        kidFamily = find_individual(sibling,defaultdict = individualsDict)['spouse']
        if kidFamily != 'NA':
            niecesAndNephews += find_family(kidFamily, defaultdict = familiesDict)['children']

    if find_family(person['spouse'], defaultdict = familiesDict)['husbandId'] in niecesAndNephews or find_family(person['spouse'], defaultdict = familiesDict)['wifeId'] in niecesAndNephews:
        return False

    return True

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

# US23: Verify unique name and birthdate
def US23_unique_name_and_birthdate(individualsDict=individualsDict):
    """Verify unique name and birthdate"""
    all_unique = True
    names_to_ids_and_birthdays = {}
    for id, individual in individualsDict.items():
        name = individual["name"]
        birthday = individual["birthday"]

        if name not in names_to_ids_and_birthdays:
            names_to_ids_and_birthdays[name] = (id, birthday)
        else:
            other_id, other_bday = names_to_ids_and_birthdays[name]
            if other_bday == birthday:
                all_unique = False
                print(f"US23-ERR: Individual {id} has same name and birthday"
                      f" as {other_id}")

    return all_unique

# US24: Unique families by spouse name and marriage date
def US24_unique_families_by_spouse(familiesDict=familiesDict):
    """Verify families are unique by spouse names and date"""
    all_unique = True
    husbands, wives = {}, {}
    for id, family in familiesDict.items():
        husband = family["husbandName"]
        wife = family["wifeName"]
        marriage_date = family["married"]

        if (husband, marriage_date) in husbands and (wife, marriage_date) in wives:
            print(f"US24-ERR: Family {id} has same spouse names and marriage"
                  f" date as family {husbands[(husband, marriage_date)]}")
            all_unique = False
        else:
            husbands[(husband, marriage_date)] = id
            wives[(wife, marriage_date)] = id

    return all_unique
    
def US25_unique_first_name_and_birthdate(family, local_inds=None):
    if local_inds == None:
        local_inds = individualsDict
    names_births = defaultdict(int)
    for child_id in family['children']:
        child = local_inds[child_id]
        first_name = child['name'].split()[0]
        birthday = child['birthday']
        names_births[(first_name, birthday)] += 1
    
    for _,count in names_births.items():
        if count > 1: return False
    return True

# US28: Order Siblings by Age
def US28_order_siblings(family):
    #default case if 0 or 1 siblings
    sorted_siblings = family['children']

    if len(family['children']) > 1:
        siblings = family['children']
        sorted_siblings = sorted(siblings, key = lambda sibling: gedcom_date_to_datetime(find_individual(sibling)['birthday']))
        
    return sorted_siblings

# US29: List deceased individuals
def US29_verify_deceased(individual):
    return not individual['alive']

# US30: List living married individuals
def US30_verify_living_married(individual):
    return individual['alive'] and individual['spouse'] != 'NA'

# US31: List living single
def US31_verify_living_single(individual):
    # if local_fams == None: 
    #     local_fams = familiesDict
    # # # Search through families and check if the individual matches any 'husbandId'
    # # def never_married(ind_id, fams):
    # #     for _, fam in fams.items():
    # #         if fam['husbandId'] == ind_id or fam['wifeId'] == ind_id: return False
    # #     return True
    return individual['alive'] and individual['spouse'] == 'NA'
# US32 List multiple births
def US32_get_multiple_births(family):
    births = {}
    for cid in family['children']:
        child = find_individual(cid)
        births.setdefault(child['birthday'], []).append(cid)
    groups = []
    for children in births.values():
        if len(children) >= 2:
            groups.append(children)
    return groups

# US33: List all orphaned children
def US33_verify_orphans(individual):
    if individual['child'] == 'NA':
        return False
    parentsFamily = find_family(individual['child'])
    father = find_individual(parentsFamily['husbandId'])
    mother = find_individual(parentsFamily['wifeId'])
    childAge =  individual['age']
    return father['alive'] == False and mother['alive'] == False and childAge < 18

# US34: List large age differences couples
def US34_verify_large_age_differences_couples(family):
    husbandAge = find_individual(family['husbandId'])['age']
    wifeAge = find_individual(family['wifeId'])['age']
    return not husbandAge >= wifeAge * 2 or wifeAge >= husbandAge * 2

# US35: List recent births
def US35_verify_birth_at_recent_30_days(individual):
    today = datetime_to_gedcom_date(datetime.now())
    return dates_within(individual['birthday'], today, 30, 'days')

# US36: List recent deaths
def US36_verify_death_at_recent_30_days(individual):
    today = datetime_to_gedcom_date(datetime.now())
    return (not individual['alive']) and dates_within(individual['death'], today, 30, 'days')
    #print(f"Family member {name} died on {person['death']}")

# US37: List recent survivors
def US37_print_all_surviors(
        individualsDict=individualsDict,
        familiesDict=familiesDict,
):
    at_least_one = False
    for id, individual in individualsDict.items():
        if US36_verify_death_at_recent_30_days(individual) == True:
            at_least_one = True
            the_dead = individual
            the_family_of_the_dead = find_family(the_dead['spouse'])
            if the_dead['gender'] == 'F':
                the_spouse_of_the_dead = find_individual(the_family_of_the_dead['husbandId'])
            else:
                the_spouse_of_the_dead = find_individual(the_family_of_the_dead['wifeId'])
            if the_spouse_of_the_dead['alive'] == True:
                print(f'Living spouse of individual {id}: ')
                print_individual(the_spouse_of_the_dead, ['id'])
            for childId in the_family_of_the_dead['children']:
                child = find_individual(childId)
                if child['alive'] == True:
                    print(f'Living descendants of individual{id}: ')
                    print_individual(child, ['id'])
    if not at_least_one:
        print("There isn't dead in recent 30 days")
    print()

# US38: List upcoming birthdays
def US38_verify_birthday_in_the_next_30_days(individual):
    if individual['alive'] == True:
        today_datetime = datetime.now()
        current_year = today_datetime.year
        this_year_birthday_datetime = gedcom_date_to_datetime(individual['birthday']).replace(year=current_year)
        today = datetime_to_gedcom_date(today_datetime)
        this_year_birthday = datetime_to_gedcom_date(this_year_birthday_datetime)
        return dates_within(this_year_birthday, today, 30, 'days')
 
#US39: List upcoming anniversaries
def US39_verify_upcoming_anniversaries_30_days(individual, familiesDict = familiesDict):
    if individual['spouse'] == "NA": 
        return False
    family = find_family(individual['spouse'])
    datetime_today = datetime.now()
    today = datetime_to_gedcom_date(datetime.now())
    old_married = gedcom_date_to_datetime(family['married'])
    #set married year
    new_married = old_married.replace(year = datetime_today.year)
    
    return dates_within(datetime_to_gedcom_date(new_married), today, 30, 'days')

# US45: List families with large families
def US45_print_large_families(
        individualsDict=individualsDict,
        familiesDict=familiesDict,
):
    at_least_one = False
    for id, family in familiesDict.items():
        if len(family["children"]) > 5:
            print_family(family, None, ["id"])
            at_least_one = True

    if not at_least_one:
        print("None")

    print()
    
# US46: Count the percentage of males and females
def US46_male_female_ratio(individualsDict=individualsDict):
    male_num = 0
    female_num = 0
    for id, individual in individualsDict.items():

        if individual['gender'] == 'M':
            male_num += 1
        else:
            female_num += 1

    if male_num == 0 and female_num == 0:
        return 0,0

    Pmale = male_num / (male_num + female_num)
    Pfemale = 1 - Pmale

    return 100 * Pmale, 100 * Pfemale

# US55: Print average lifespan
def US55_get_average_lifespan(individuals):
    """
    Returns the average lifespan of a list of dead individuals.
    Skips individuals that are still alive.
    Return -1 of no dead individuals are found in the list or if the list is empty
    """
    lifespans = []
    for ind in individuals:
        if ind['alive']:
            continue

        birth = gedcom_date_to_datetime(ind['birthday'])
        death = gedcom_date_to_datetime(ind['death'])
        lifespan = death - birth
        lifespans += [lifespan.days]

    if lifespans == []:
        return -1

    return (sum(lifespans)/len(lifespans))/365
    
    
def verify():
    for id, family in familiesDict.items():
        multiple_births = US32_get_multiple_births(family)
        if multiple_births != []:
            print(f"US32-INFO: Family {id} has multiple_births:")
            for group in multiple_births:
                print(f"\t{group}")
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
        if not US13_verify_sibling_spacing(family):
            print(f"US13-ERR: Family {id} has children whose birthdays are not properly spaced")
        if not US14_verify_multiple_births(family):
            print(f"US14-ERR: Family {id} has more than 5 siblings born on the same day")
        if not US15_verify_fewer_than_15_siblings(family):
            print(f"US15-ERR: Family {id} has more than 14 siblings")
        if not US16_verify_male_last_names(family):
            print(f"US16-ERR: Family {id} has males with different last names")
        if not US18_verify_marriage_not_siblings(family):
            print(f"US18-ERR: Family {id} fails marriage between siblings check")
        if not US21_verify_marriage_gender_roles(family):
            print(f"US21-ERR: Family {id} does not pass gender roles test")
        if not US25_unique_first_name_and_birthdate(family):
            print(f"US25-ERR: Family {id} does not pass unique first name and birthdate test")
        if not US34_verify_large_age_differences_couples(family):
            print(f"US34-ERR: Family {id} has couples who are large age differences")
        print(f"US28-INFO: Family {id} siblings ordered:", US28_order_siblings(family))
        #print(US28_order_siblings(family))

    dead_individuals = []
    for id, individual in individualsDict.items():
        # US27 Include person's current age when listing individuals
        print_individual(individual, ['id', 'name', 'age'])
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
        if not US09_verify_birth_before_parents_death(individual):
            print(f"US09-ERR: Individual {id} was born after their mother died, or too long after their father died")
        if not US17_verify_no_marriage_to_descendants(individual):
            print(f"US29-INFO: Individual {id} is married to one of their decendants")
        if not US19_verify_no_first_cousin_marriage(individual):
            print(f"US19-ERR: Individual {id} is married to their first cousin")
        if not US20_verify_aunts_and_uncles(individual):
            print(f"US20-ERR: Individual {id} is married to their niece of nephew")
        if US29_verify_deceased(individual):
            print(f"US29-INFO: Individual {id} is deceased")
            dead_individuals += [individual]
        if US30_verify_living_married(individual):
            print(f"US30-INFO: Individual {id} is living and married")
        if US31_verify_living_single(individual):
            print(f"US31-INFO: Individual {id} is living and has never been married")
        if US33_verify_orphans(individual):
            print(f"US33-INFO: Individual {id} is an orphan")
        if US35_verify_birth_at_recent_30_days(individual):
            print(f"US35-INFO: Individual {id} was born within 30 days")
        if US36_verify_death_at_recent_30_days(individual):
            print(f"US36-INFO: Individual {id} has died within 30 days")
        if US38_verify_birthday_in_the_next_30_days(individual):
            print(f"US38-INFO: Individual {id} has birthday in the next 30 days")
        if US39_verify_upcoming_anniversaries_30_days(individual):
            print(f"US39-INFO: Individual {id}'s anniversary is within 30 days")

    US23_unique_name_and_birthdate()  # operate on all individuals at once

    US46_male_female_ratio()
    US24_unique_families_by_spouse(familiesDict=familiesDict)

    print("Large Families:")
    US45_print_large_families()

    US37_print_all_surviors()

    print("Average Lifespan: ", end="")
    avg_lifespan = US55_get_average_lifespan(dead_individuals)
    if avg_lifespan < 0:
        print("NA")
    else:
        print(str(avg_lifespan) + " years")
