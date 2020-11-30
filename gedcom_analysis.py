import sys
from parse import parse_gedcom_file_03
from verifier import verify, initialize_verifier, print_notes

def main():
    gedcom_file = sys.argv[1]
    individuals, families = parse_gedcom_file_03(gedcom_file)
    initialize_verifier(individuals, families)
    verify()
    print_notes()

if __name__ == '__main__':
    main()
