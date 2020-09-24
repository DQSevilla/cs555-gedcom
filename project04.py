
def ensureMarriageGenderRoles(ind1, ind2):
    """Checks if a marriage is between a male and a female.

    Parameters
    ----------
    ind1 : dict
        the first individual in the marriage
    ind2 : dict
        the second individual in the marriage

    Returns
    -------
    bool
        True if the marriage is valid. False otherwise.
    """
    
    valid_genders = ["M", "F"]
    gender1 = ind1.get("gender")
    gender2 = ind2.get("gender")

    if gender1 is None or gender2 is None:
        return False

    if not (gender1 in valid_genders and gender2 in valid_genders):
        return False

    if gender1 == gender2:
        return False

    return True
