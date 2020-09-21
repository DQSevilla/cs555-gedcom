class Individual:
    def __init__(self, iid, name, gender, birthday, age, death, child, spouse):
        self.id = iid
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.alive = True if death != 'NA' else False 
        self.death = death
        self.child = child
        self.spouse = spouse 