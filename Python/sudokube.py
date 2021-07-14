import copy, time, cProfile, pstats, json, itertools
from collections import OrderedDict
time0 = time.time()
######
##
## GLOBALS
##
######
Locs = ['TL', 'TC', 'TR',
        'ML', 'MC', 'MR',
        'BL', 'BC', 'BR']

options = {}
options['TL'] = [1,1,3,3,4,9]
options['TC'] = [3,4,5,7,8,9]
options['TR'] = [1,2,2,6,7,7]
options['ML'] = [2,2,4,6,7,8]
options['MC'] = [1,1,4,5,6,7]
options['MR'] = [1,3,3,5,8,9]
options['BL'] = [5,5,6,7,8,9]
options['BC'] = [2,2,3,6,8,9]
options['BR'] = [4,4,5,6,8,9]
allowed_doubles = [[1,3],[],[2,7],[2],[1],[3],[5],[2],[4]]

class Face:
    def __init__(self, contents):
        if len(contents) != 9:
            raise ValueError("Face length not right length:", contents)
        self.face = contents
        
######
##
## Q1: HOW MANY FACES?
##  A: 16720! whoa (1865 with out duplicate faces)
##
######


## Ex.                 [1,2] -> [ [1],[2] ]
#             [1,2,4], [4,5] -> [ [1, 4], [1, 5], [2, 4], [2, 5], [4, 5] ]
#  [['a','b'],[1,2,4],[4,5]] -> [ ['a', 1, 4], ['a', 1, 5], ['a', 2, 4], ['a', 2, 5], ['a', 4, 5],
#                                 ['b', 1, 4], ['b', 1, 5], ['b', 2, 4], ['b', 2, 5], ['b', 4, 5] ]  
def appendAll(LoLists):
    if len(LoLists) == 1:
        return [[x] for x in LoLists[0]]
    else:
        front = LoLists[0]
        rest = appendAll(LoLists[1:])
        # one line, without checking
        result = [[x] + y for x in front for y in rest if x not in y]
        return result

def store_faces(file):
    with open(file, 'w') as f:
        for i in good_faces:
            f.write(str(i) + "\n")

pruned_options = {}
for loc in Locs:
    buffer = []
    pruned_options[loc] = [buffer.append(x) or x for x in options[loc] if x not in buffer]

good_faces = appendAll( [pruned_options[key] for key in Locs] )

#store_faces('faces.txt')

######
##
## Q2: HOW MANY VALID SETS OF 6 FACES?
##  A: ?????
#  1:303 2:31216 3:1139430 4:11107900 5~18883430 6 = 5
##
######

# NOTE: good_faces defined in Q1
A = [x for x in good_faces if x[1] == 3]
B = [x for x in good_faces if x[1] == 4]
C = [x for x in good_faces if x[1] == 5]
D = [x for x in good_faces if x[1] == 7]
E = [x for x in good_faces if x[1] == 8]
F = [x for x in good_faces if x[1] == 9]

# Naive way to produce triples.
# It doesn't hash. It's not the fastest,
# but it's only a few lines long and it gets the right triples
def iter_three(f,s,t):
    time0 = time.time()

    pairs = [list(i) for i in itertools.product(f,s) if not conflict(i[0], i[1])]
    triples = [i[0] + [i[1]] for i in itertools.product(pairs,t) if verify_three( i[0] + [i[1]] ) ]

    checks = len(f) * len(s) + len(pairs) * len(t)
    print(len(triples), ",", checks, ",", time.time() - time0)
    return triples

# Unique options and list making by using decimals in place of duplicates
'''
    unique_ops = {}
    unique_ops['TL'] = [1,1.1,3,3.1,4,9]
    unique_ops['TC'] = [3,4,5,7,8,9]
    unique_ops['TR'] = [1,2,2.1,6,7,7.1]
    unique_ops['ML'] = [2,2.1,4,6,7,8]
    unique_ops['MC'] = [1,1.1,4,5,6,7]
    unique_ops['MR'] = [1,3,3.1,5,8,9]
    unique_ops['BL'] = [5,5.1,6,7,8,9]
    unique_ops['BC'] = [2,2.1,3,6,8,9]
    unique_ops['BR'] = [4,4.1,5,6,8,9]

    def round_appendAll(LoLists):
        if len(LoLists) == 1:
            return [[x] for x in LoLists[0]]
        else:
            result = []
            front = LoLists[0]
            rest = round_appendAll(LoLists[1:])
            result = [[x] + y for x in front for y in rest if int(x) not in map(int,y)]
            return result
        
    dec_faces = round_appendAll( [unique_ops[key] for key in Locs] )

    dec_A = [x for x in dec_faces if x[1] == 9]
    dec_B = [x for x in dec_faces if x[1] == 8]
    dec_C = [x for x in dec_faces if x[1] == 4]
    dec_D = [x for x in dec_faces if x[1] == 5]
    dec_E = [x for x in dec_faces if x[1] == 3]
    dec_F = [x for x in dec_faces if x[1] == 7]
'''
##
##                  FILE READ/WRITE METHOD
##
##
##
##

#
# Take in a [List of Faces] and the current [List of Sets] and start appending
# Also takes the current point, default to zero, so if I end it early I know
# where to start back up.
#
def add_to_back(LoSets, LoFaces, curr = 0, end = None):
    time0 = time.time()
    checks = 0
    result = []
    read_good_dict(LoFaces)
    #do_sets = LoSets[curr:]
    for set in LoSets[curr:end]:
        keys = [get_key(face) for face in set]
        for candidate in key_list_gen(keys):
            valid = True
            for pair in itertools.combinations(set, 2):
                checks = checks + 1
                valid = valid and verify_three(list(pair) + [candidate])
            if valid:
                result.append(set + [candidate])
        curr = curr + 1
        if curr % int(len(LoSets) / 10) == 0:
            print("At", curr, "of", len(LoSets))
    print(len(result), ",", checks, ",", time.time()-time0)
    return result    

##
##                  HASH CHECKING METHOD
##
##  Pick a face from A...F, go to the next bucket, pick again, etc.
##  Only need to pick 5 if I can generate 6th.
##  O(N**5) where N is number of faces being considered: len(good_faces)
##

#
# If two faces share a number that isn't allowed then reject the pairing.
#
def conflict(face, Face): # -> bool
    for i in [0,2,3,4,5,6,7,8]:
        if (face[i] == Face[i]):
            if face[i] not in allowed_doubles[i]:
                return True
    return False

#
# Do a full conflict check on three faces
# If this can be faster then everything will run quicker.
#
def verify_three(LoFaces): # -> bool
    a = LoFaces[0]
    b = LoFaces[1]
    c = LoFaces[2]
    for i in [0,2,3,4,5,6,7,8]: # 1 is guaranteed to be fine
        if c[i] == a[i] or c[i] == b[i]:
            if c[i] not in allowed_doubles[i]:
                return False
            if a[i] == b[i]:
                return False
        ## Slows down verify(), but still faster than an extra conflict()
        if a[i] == b[i]:
            if a[i] not in allowed_doubles[i]:
                return False
    return True

#
# Current fastest way to combine faces from the three arguments into a
#   valid set of faces. Naive algorithm with (n**3?) comparisons
#
def hash_three(first, second, third): # -> list
    temp1 = []
    temp2 = []
    final = []
    time0 = time.time()

    read_good_dict(second)

    Q = 0
    key_list = []
    for a in first:
        for key in good_dict.keys():
            if key == 1 or key != get_key(a):
                key_list = good_dict[key]
                for b in key_list:
                    Q = Q+1
                    if not conflict(a,b):
                        temp2.append([a,b])
                

    read_good_dict(third)

    Qv = 0
    temp1 = []
    for t in temp2:
        for key in good_dict.keys():
            if key == 1 or (key not in [get_key(t[0]), get_key(t[1])]):
                key_list = good_dict[key]
                for c in key_list:
                    Qv = Qv+1
                    hold = t + [c]
                    if verify_three(hold):
                        temp1.append(hold)

    Q = Q + Qv
    final = temp1
    
    print(len(final),",",Q,",",time.time() - time0)
    return final

def hash_two(first, second): 
    final = []
    time0 = time.time()

    read_good_dict(second)

    Q = 0
    key_list = []
    for a in first:
        for key in good_dict.keys():
            if key == 1 or key != get_key(a):
                key_list = good_dict[key]
                for b in key_list:
                    Q = Q+1
                    if not conflict(a,b):
                        final.append([a,b])
    
    print(len(final),",",Q,",",time.time() - time0)
    return final

def hash_test(first, second, third): # -> list
    temp1 = []
    final = []
    time0 = time.time()

    read_good_dict(second)
    Q = 0
    for a in first:
        for b in key_list_gen([get_key(a)]):
            Q = Q+1
            if not conflict(a,b):
                temp1.append([a,b])
                
    read_good_dict(third)
    Qv = 0
    for t in temp1:
        for c in key_list_gen( [get_key(t[0]), get_key(t[1])] ):
            Qv = Qv+1
            hold = t + [c]
            if verify_three(hold):
                final.append(hold)

    Q = Q + Qv
    print(len(final),",",Q,",",time.time() - time0)
    return final

#
# Hashing Helpers
#
def get_key(face): # -> int
    '''the key is just MC because TC is already sorted into A...F'''
    return face[4]

# Sort "given" by get_key() into global good_dict{}
def read_good_dict(given):
    global good_dict
    good_dict = {}
    for f in given:
        key = get_key(f)
        try:
            good_dict[key].append(f)
        except KeyError:
            good_dict[key] = [f]

def key_list_gen(avoid_keys):
    for key in good_dict.keys():
        if key == 1 or key not in avoid_keys:
            key_list = good_dict[key]
            for b in key_list:
                yield(b)

def whats_left(LoFaces):
    orig_ops = [options[key] for key in Locs]
    set_ops = copy.deepcopy(orig_ops)
    for i in range(9):
        for face in LoFaces:
            set_ops[i].remove(face[i]) 
    
    return set_ops

def prob_two(one, two):
    return len(hash_two(one,two))/(len(one)*len(two))


profile = cProfile.Profile()
profile.enable()
#
# End Doc Profiling code
#
'''
print("sets, conflict checks, time")

print("AB", prob_two(A,B))
print("AC", prob_two(A,C))
print("AD", prob_two(A,D))
print("AE", prob_two(A,E))
print("AF", prob_two(A,F))
print("BC", prob_two(B,C))
print("BD", prob_two(B,D))
print("BE", prob_two(B,E))
print("BF", prob_two(B,F))
print("CD", prob_two(C,D))
print("CE", prob_two(C,E))
print("CF", prob_two(C,F))
print("DE", prob_two(D,E))
print("DF", prob_two(D,F))
print("EF", prob_two(E,F))
'''


# pairs = [list(i) for i in itertools.product(A, B) if not conflict(i[0], i[1])]
#pairs = list(itertools.product(A, B))
hi = iter_three(A,B,C)
print(len(hi), time.time() - time0)    


'''
DE = hash_two(D,E)
with open('Face Files/DE.txt', 'w') as f:
        for i in DE:
            f.write(str(i) + "\n")
'''
'''
DEF = add_to_back(DE, F)
with open('Face Files/DEF.txt', 'w') as f:
        for i in DEF:
            f.write(str(i) + "\n")
'''

'''
with open('Face Files/DEF.txt', 'r') as f:
        DEF = f.readlines()
DEF = [json.loads(i) for i in DEF] #convert the string versions of each line into lists

DEFC10000 = add_to_back(DEF, C, 1000000)

with open('Face Files/DEFC.txt', 'a') as f:
        for i in DEFC10000:
            f.write(str(i) + "\n")
'''

'''
with open('Face Files/DEFC.txt', 'r') as f:
    for runs in range(100):
        DEFC = []
        end = 107079
        # Read in 1% of DEFC
        for i in range(end):
            DEFC.append(f.readline())

        #convert the string versions of each line into lists
        DEFC = [json.loads(i) for i in DEFC]

        # Match with Bs
        DEFCB = add_to_back(DEFC, B)
'''

profile.disable()
'''
p = pstats.Stats(profile)
p.strip_dirs().sort_stats('time').print_stats(10)
p.sort_stats('time').print_callers(3)
'''