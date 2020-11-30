"""
Common utilities such as date and time conversions
"""
from datetime import datetime
from typing import Dict, List


def print_individual(individual : Dict[str, str], keys: List[str], individualsDict):
    """
    Prints an individual (color-coded by name) and any additional
    information along with it
    """
    ind_str = ""
    for index, key in enumerate(keys):
        if index != 0:
            ind_str += ", "

        if key == 'name':

            #US47 twins special symbol
            twins = {}
            for id, i in individualsDict.items():
                family = i["child"]
                birthday = i["birthday"]

                if family+birthday in twins:
                    twins[family+birthday] = twins[family+birthday].append(i['id'])
                else:
                    twins[family+birthday] = [i['id']]

            flatList = []
            for twin_lists in twins.values():
                if len(twin_lists) > 1:
                    flatList = flatList + twin_lists

            # US44: underline if dead
            if not individual["alive"]:
                ind_str += "\u001b[4m"
            # blue for boy, red for girl
            ind_str += "\033[1;34;40m" if individual["gender"] == "M" else "\033[1;35;40m"
            ind_str += f"name = {individual['name']}\033[0;37;40m" # reset color
            ind_str += "\u001b[0m" # reset text decoration
            
            if individual['id'] in flatList:
                ind_str += u'\1071'
        else:
            ind_str += f"{key} = {individual[key]}"

        if key == 'birthday':
            ind_str += format_date(individual['birthday'])

    print(ind_str)

def format_date(date : str):
    """
    Prints the date in eu format dd-mm-yyyy
    """
    splitDate = date.split()
    if splitDate[0].isalpha():
        splitDate[0],splitDate[1] = splitDate[1],splitDate[0]

    ret = " ".join(splitDate)
    
    return ret

def print_family(family : Dict[str, str], ind_keys : List[str], fam_keys : List[str]):
    """
    Prints a family
    """
    fam_str = ""
    for index, key in enumerate(fam_keys):
        if index != 0:
            fam_str += ", "

        fam_str += f"{key} = {family[key]}"

    print(fam_str)

def gedcom_date_to_datetime(gedcom_date : str) -> datetime:
    """
    Convert a GEDCOM date string to a Python datetime object

    Args:
        gedcom_date (str): a GEDCOM date string e.g. "01 JAN 1970"

    Returns:
        a datetime.datetime representation of the date string
    """
    try:
        return datetime.strptime(gedcom_date, "%d %b %Y")
    except:
        print(f"PARSER-ERR: Date {gedcom_date} is invalid. Defaulting to 1/1/70.")
        return datetime.strptime('1 JAN 1970', "%d %b %Y")



def datetime_to_gedcom_date(date : datetime) -> str:
    """
    Convert a Python datetime object to a gedcom date string

    Args:
        date (datetime): a datetime.datetime object

    Returns:
        a GEDCOM compatible date string
    """
    return date.strftime("%d %b %Y").upper()

def date_occurs_before(gedcom_date_first : str, gedcom_date_second : str) -> bool:
    """
    Checks whether the first gedcom date occurs before the second one

    Args:
        gedcom_date_first (str): A gedcom string date e.g. "1 JAN 1970"
        gedcom_date_second (str): A gedcom string date e.g. "1 JAN 1970"

    Returns:
        a boolean, true if gedcom_date_first occurs before gedcom_date_second, false otherwise
    """
    date_first = gedcom_date_to_datetime(gedcom_date_first)
    date_second = gedcom_date_to_datetime(gedcom_date_second)

    return date_first < date_second

def date_occurs_before_cond(gedcom_date_first : str, gedcom_date_second : str, cond : str) -> bool:
    """
    Checks whether the first gedcom date occurs before the second one
    If cond is NA, we return true by default

    Args:
        gedcom_date_first (str): A gedcom string date e.g. "1 JAN 1970"
        gedcom_date_second (str): A gedcom string date e.g. "1 JAN 1970"
        cond (str): A field in the gedcom file that could possibly be NA

    Returns:
        a boolean, true if gedcom_date_first occurs before gedcom_date_second, or cond == 'NA'
        false otherwise
    """

    return cond == 'NA' or date_occurs_before(gedcom_date_first, gedcom_date_second)

def dates_within(
    gedcom_date_first : str,
    gedcom_date_second : str,
    limit : int,
    units : str
) -> bool:
    """
    Checks whether two dates are within limit units of each other

    Args:
        gedcom_date_first (str): A gedcom string date e.g. "1 JAN 1970"
        gedcom_date_second (str): A gedcom string date e.g. "1 JAN 1970"
        limit (int): an amount of time e.g. 150
        units (str): a measurement of time e.g. days

    Returns:
        True if dt1 and dt2 are within limit units where:
            dt1, dt2 are instances of datetime
            limit is a number
            units is a string in ('days', 'months', 'years')
    """

    conversion = {'days': 1, 'months': 30.4, 'years': 365.25}

    dt1 = gedcom_date_to_datetime(gedcom_date_first)
    dt2 = gedcom_date_to_datetime(gedcom_date_second)

    return (abs((dt1 - dt2).days) / conversion[units]) <= limit

def dates_within_cond(
    gedcom_date_first : str,
    gedcom_date_second : str,
    limit : int,
    units : str,
    cond : str
) -> bool:
    """
    Checks whether two dates are within limit units of each other
    If cond is NA, we return true by default

    Args:
        gedcom_date_first (str): A gedcom string date e.g. "1 JAN 1970"
        gedcom_date_second (str): A gedcom string date e.g. "1 JAN 1970"
        limit (int): an amount of time e.g. 150
        units (str): a measurement of time e.g. days
        cond (str): A field in the gedcom file that could possibly be NA


    Returns:
        True if cond == NA or, dt1 and dt2 are within limit units where:
            dt1, dt2 are instances of datetime
            limit is a number
            units is a string in ('days', 'months', 'years')
    """

    return cond == 'NA' or dates_within(gedcom_date_first, gedcom_date_second, limit, units)
