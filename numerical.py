
from random import *
def big():
    return str(choice([ i for i in range(6,10)]))

def small():
    return str(choice([i for i in range(1,6)]))

def all():
    return str(choice([i for i in range(0,10)]))

level1 = all()+'+'+all()
level2 = big()+'-'+small()
level3 = all()+'x'+all()

level3_a = small()+small()+"+"+small()
level4 = small()+small()+'+'+small()+small()
level5 = big()+big()+'+'+big()+big()

level5_a = small()+small()+'-'+big()
level6 = big()+all()+'-'+small()+all()
level7 = big()+big()+'-'+small()+big()

level8 = small()+small()+'x'+small()
level9 = small()+small()+'x'+big()
level10 = small()+big()+'x'+big()
level11 = big()+big()+'x'+big()
level12 = small()+small()+'x'+small()+small()

LEVELS = [level1,level2,level3,level3_a,level4,level5,level5_a,level6,
            level7,level8,level9,level10,level11,level12]

QUESTION = LEVELS[3]
print(QUESTION.replace('x','*'))
print(QUESTION)