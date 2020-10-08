"""
GEDCOM file parsing (and eventually writing) utilities
"""
#from prettytable import PrettyTable

VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
              'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE',
              'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
IGNORE_TAGS = ['HEAD', 'TRLR', 'NOTE']
DATE_TAGS = ['BIRT', 'DEAT', 'DIV', 'MARR']
IND_TAGS = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
FAM_TAGS = ['HUSB', 'WIFE','CHIL', 'DIV', 'DATE']


def parse_gedcom_file(file_path : str):
    """
    Parse the GEDCOM file at the given path into a dict
    TODO: Pick better representations for the in-memory structures

    Args:
        file_path (str): path to a GEDCOM file

    Returns:
        TODO
    """
    with open(file_path, "r") as file:
        entries = [line.strip().split(" ") for line in file.readlines()]

    for entry in entries:
        # The entry's tag is item 3 if INDI or FAM is present without FAMS
        # and FAMC. Otherwise it is the second item
        tag_index = 2 if "INDI" in entry or (
            "FAM" in entry and not ("FAMS" in entry or "FAMC" in entry)
        ) else 1

        tag = entry[tag_index]
        level = entry[0]

        # skip invalid or useless tags
        if tag not in VALID_TAGS or (
            level == "1" and tag == "DATE" or
            level == "2" and tag == "NAME"
        ):
            continue

        if tag in ["INDI", "FAM"]:
            print("Indi or Fam tag: TODO")


if __name__ == "__main__":
    parse_gedcom_file("cs555project03.ged")
