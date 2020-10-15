GEDCOM_FILE = 'cs555project01.ged'
VALID_TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT',
              'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE',
              'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']

def processFile(file):
    lines = []
    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace('\n','')
        # Input Echo
        print('--> {0}'.format(line))

        #Output Process
        tag_index = 2 if 'INDI' in line or ('FAM' in line and 'FAMS' not in line and 'FAMC' not in line) else 1
        fields = line.split(' ')
        tag = fields[tag_index]
        valid = 'Y' if tag in VALID_TAGS else 'N'
        level = fields[0]
        fields.pop(tag_index)
        fields.pop(0)
        print('<-- {0}|{1}|{2}|{3}'.format(level, tag, valid, ' '.join(fields)))

def main():
    processFile(GEDCOM_FILE)

if __name__ == '__main__':
    main()

