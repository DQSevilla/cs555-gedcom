import sys
from parse import parse_gedcom_file_03
from verifier import verify, initialize_verifier

def main():
    gedcom_file = sys.argv[1]
    individuals, families = parse_gedcom_file_03(gedcom_file)
    initialize_verifier(individuals, families)
    verify()

if __name__ == '__main__':
    main()
