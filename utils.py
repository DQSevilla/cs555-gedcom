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
    return date.strftime("%d %b %Y")
