"""
Common utilities such as date and time conversions
"""
from datetime import datetime


def gedcom_date_to_datetime(gedcom_date : str) -> datetime:
    """
    Convert a GEDCOM date string to a Python datetime object

    Args:
        gedcom_date (str): a GEDCOM date string e.g. "01 JAN 1970"

    Returns:
        a datetime.datetime representation of the date string
    """
    return datetime.strptime(gedcom_date, "%d %b %Y")


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
