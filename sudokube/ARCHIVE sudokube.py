#############################################################################################
##
## 
##
## This Archive of the sudokube code was made Friday May 8 2020
## The "hash" method can produce pairs instantly and 1,320,772 BCD triples in 14.15 seconds
## Currently halting progress is any ability to get sets of 5 faces in a timely manner.
## 
##
##
#############################################################################################


import copy, time, cProfile, pstats
from collections import OrderedDict
#from pstats import SortKey

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
##  A: 16720! whoa (with duplicates, 1865 w/o)
##
######
def appendAll(LoLists):
    if len(LoLists) == 1:
        return [[x] for x in LoLists[0]]
    else:
        front = LoLists[0]
        rest = appendAll(LoLists[1:])
        # one line, without checking
        result = [[x] + y for x in front for y in rest if x not in y]
        return result
# TESTS
'''
print(appendAll([]))
print(appendAll([[1,2]]))
print(appendAll([[1,2,3], [4,5]]))
print(appendAll([['a','b'],[1,2,4],[4,5]]))
'''

pruned_options = {}
for loc in Locs:
    buffer = []
    pruned_options[loc] = [buffer.append(x) or x for x in options[loc] if x not in buffer]

good_faces = appendAll( [pruned_options[key] for key in Locs] )
#print(len(good_faces))


# Removing duplicates. Not needed with pruned options.
'''
start = time.time()
all_faces = appendAll( [options[key] for key in Locs] )
mid = time.time()
wo_dups = [] 
[wo_dups.append(x) for x in all_faces if x not in wo_dups]
print(len(all_faces), len(wo_dups), time.time()- mid, mid - start)
'''

######
##
## Q2: HOW MANY VALID SETS OF 6 FACES?
##  A: ?????
##
######
'''
def remove_all_val(the_list, val):
   return [value for value in the_list if value != val]

def get_number(options, so_far):
    if len(options) == 0:
        return None
    i = 0
    n = options[i]
    while n in so_far and i < len(options):
        n = options[i]
        i = i + 1
    if i == len(options):
        return None
    return n

def partial_face(PT_OPS, FACE):
    if len(PT_OPS) == 0:
        return FACE
    elif len(PT_OPS[0]) == 0:
        # if options empty, no completion possible
        return None
        
    face_cp = copy.deepcopy(FACE)
    ops_cp = copy.deepcopy(PT_OPS)

    # first guess
    store = get_number(ops_cp[0], face_cp)

    # if get_number fails then try other completions
    while store == None:   
        ops_cp[0] = remove_all_val(ops_cp[0], ops_cp[0][0])   
        if len(ops_cp[0]) == 0:
            # if options empty, no completion possible
            return None
        store = get_number(ops_cp[0], face_cp)
        
    face_cp.append(store)
    check_face = partial_face(ops_cp[1:], face_cp)
    
    while check_face == None:
        if len(ops_cp[0]) == 0:
            return None
        ops_cp[0] = remove_all_val(ops_cp[0], ops_cp[0][0])
        # if partial_face fails then change current completion
        check_face = partial_face(ops_cp, FACE)
    
    return check_face

def make_face(all_ops):
    face = []
    result = partial_face(all_ops, face)
    return result


OPTIONS = [options[key] for key in Locs]
faces = [None] * 6

for index in range(6):
    faces[index] = make_face(OPTIONS)
    for i in range(6):
        if faces[index] == None:
            break
        OPTIONS[i].remove(faces[index][i])

#print(faces)
'''



# NOTE: good_faces defined in Q1
A = [x for x in good_faces if x[1] == 3]
B = [x for x in good_faces if x[1] == 4]
C = [x for x in good_faces if x[1] == 5]
D = [x for x in good_faces if x[1] == 7]
E = [x for x in good_faces if x[1] == 8]
F = [x for x in good_faces if x[1] == 9]
#
# A way to check if a face conflicts with a face in LoFaces. Only compares pairs.
#
''' 
def O_conflicts(face, LoFaces) -> bool:
    for Face in LoFaces:
        if conflict(face, Face):
            return True
    return False

def O_conflict(face, Face): # -> bool
    for i in [0,2,3,4,5,6,7,8]:
        if (face[i] == Face[i]):
            if face[i] not in allowed_doubles[i]:
                return True
    return False

 OLD VERIFY THREE 
def O_verify_three(LoFaces) -> bool:
    hold = []
    hold = list(zip(LoFaces[0],LoFaces[1],LoFaces[2]))
    for x,y,z in hold:
        if x == y == z:
            return False
    return True


 OLD FAST COMBINE 
def O_combine_three(first, second, third) -> list:
    temp1 = []
    temp2 = []
    final = []
    time0 = time.time()
    #for a in first:
    #    temp1.append(a)
    temp1 = copy.copy(first)
    #time1 = time.time()

    for t in temp1:
        for b in second:
            if not O_conflict(t, b):
                temp2.append([t, b])
    #time2 = time.time()
    #temp2 = [ [t,b] for t in first for b in second if not conflict(t,b)]

    temp1 = []
    for t in temp2:
        for c in third:
            if not O_conflict(t[0], c) and not O_conflict(t[1], c):
                temp1.append(t + [c])
    #time3 = time.time()

    final = [x for x in temp1 if O_verify_three(x)]
    
    print(len(final), time.time() - time0)
    return final
'''

#
# If two faces share a number that isn't allowed then reject the pairing.
# If this can be faster then this will run quicker.
#
def conflict(face, Face): # -> bool
    for i in [0,2,3,4,5,6,7,8]:
        if (face[i] == Face[i]):
            if face[i] not in allowed_doubles[i]:
                return True
    return False

#
# Do a full conflict check on three faces
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
        ## Might take the place of conflict()
        #if a[i] == b[i]:
        #    if a[i] not in allowed_doubles[i]:
        #        return False
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
    
    print(len(final),", ",Q,", ",time.time() - time0)
    return final

def hash_two(first, second): # -> list
    #temp1 = []
    #temp2 = []
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
    #final = temp2
    print(len(final),", ",Q,", ",time.time() - time0)
    return final

#
# Hashing version
#
def get_key(face): # -> int
    '''the key is just MC because TC is already sorted'''
    return face[4]

def read_good_dict(given):
    global good_dict
    good_dict = {}
    for f in given:
        key = get_key(f)
        try:
            good_dict[key].append(f)
        except KeyError:
            good_dict[key] = [f]


def count_in():
    keys = good_dict.keys()
    counting = {}
    for i in keys:
        counting[i] = len(good_dict[i])
    return counting


def simple_three(first, second, third):
    time0 = time.time()
    good = 0
    total = 0
    final = []
    for a in first:
        for b in second:
            if not conflict(a,b):
                for c in third:
                    total = total + 1
                    if verify_three([a,b,c]):
                        good = good + 1
                        final.append([a,b,c])

    print(good,", ",total,", ",time.time() - time0)
    return final


#
# NOT WORKING
# needs to check more 3s (ex. if B and D have double, currently allows F to have same double)
# 
def make_five(Lo3, Lo2, i):
    time0 = time.time()
    final = []
    Q = 0
    for ef in Lo2[:i]:
        for bcd in Lo3[:(45*i)]:
            Q = Q + 1
            if verify_three(ef + [bcd[0]]):
                Q = Q + 1
                if verify_three(ef + [bcd[1]]):
                    Q = Q + 1
                    if verify_three(ef + [bcd[2]]):
                        final.append(bcd + ef)

    print(len(final),", ",Q,", ",time.time() - time0)
    return final

profile = cProfile.Profile()
profile.enable()
#
# End Doc Profiling code
#
print("sets, conflict checks, time")
'''for i in [50, 100, 150, 200, 300]:
    print(i, end=" ")
    DEF = hash_three2(D[:i],E[:i],F[:i])
    print(i, end=" ")
    DEF = hash_three2(D[:i],E[:i],F[:i])
    print(i, end=" ")
    DEF = hash_three2(D[:i],E[:i],F[:i])
'''
BCD = hash_three(B,C,D)
EF = hash_two(E,F)
#together = make_five(BCD,EF, 800)


profile.disable()
'''
Valid Arg 	Meaning
'calls' 	call count
'cumulative' 	cumulative time
'cumtime' 	cumulative time
'file'          file name
'filename' 	file name
'module' 	file name
'ncalls' 	call count
'pcalls' 	primitive call count
'line' 	        line number
'name' 	        function name
'nfl' 	        name/file/line
'stdname' 	standard name
'time' 	        internal time
'tottime' 	internal time
'''
p = pstats.Stats(profile)
p.strip_dirs().sort_stats('time').print_stats(10)
p.sort_stats('time').print_callers(3)

