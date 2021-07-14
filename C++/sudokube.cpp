#pragma once
#include "helpers.h"
using namespace std;
/*
*
* Globals
*
*/
const string Locs [9] = {"TL","TC","TR","ML","MC","MR","BL","BC","BR"};



unordered_map<string, vector<NUM>> options = {
    {"TL", vector<NUM>{1,1,3,3,4,9}},
    {"TC", vector<NUM>{3,4,5,7,8,9}},
    {"TR", vector<NUM>{1,2,2,6,7,7}},
    {"ML", vector<NUM>{2,2,4,6,7,8}},
    {"MC", vector<NUM>{1,1,4,5,6,7}},
    {"MR", vector<NUM>{1,3,3,5,8,9}},
    {"BL", vector<NUM>{5,5,6,7,8,9}},
    {"BC", vector<NUM>{2,2,3,6,8,9}},
    {"BR", vector<NUM>{4,4,5,6,8,9}} };
const vv<NUM> allowed_doubles = {{ {1,3},{},{2,7},{2},{1},{3},{5},{2},{4} }};




/*####
##
## Q1: HOW MANY FACES?
##  A: 16720! whoa (1865 with out duplicate faces)
##
######

## Ex.                 [1,2] -> [ [1],[2] ]
#             [1,2,4], [4,5] -> [ [1, 4], [1, 5], [2, 4], [2, 5], [4, 5] ]
#  [['a','b'],[1,2,4],[4,5]] -> [ ['a', 1, 4], ['a', 1, 5], ['a', 2, 4], ['a', 2, 5], ['a', 4, 5],
#                                 ['b', 1, 4], ['b', 1, 5], ['b', 2, 4], ['b', 2, 5], ['b', 4, 5] ]  
*/



vv<NUM> appendAll( vv<NUM> LoLists ){
    vv<NUM> ret;
    if (LoLists.size() == 1) {
        for (auto& x : LoLists[0]){
            ret.push_back( vector<NUM>{x});
        }
    } else {
        vector<NUM> front = LoLists[0];
        vv<NUM> A(LoLists.begin() + 1, LoLists.end());
        vv<NUM> rest = appendAll(A);
        for (auto& x: front){
            for (auto& y: rest){
                if (aNotInB(x, y)) {
                    vector<NUM> X{x};
                    X.insert( X.end(), y.begin(), y.end());
                    ret.push_back(X);
                }
            }
        }
    }
    return ret;
}

/* Chose to omit store_faces(file) at this time */

/*####
##
## Q2: HOW MANY VALID SETS OF 6 FACES?
##  A: ?????
#  1:303 2:31216 3:1139430 4:11107900 5~18883430 6 = 5
##
####*/

vv<NUM> copy_when(vv<NUM> from, NUM match){
    vv<NUM> ret;
    auto pred = [match](vector<NUM> num) {return num[1] == match;};
    copy_if(from.begin(), from.end(), back_inserter(ret), pred);
    return ret;
}

vector<LoFaces> iter_three(LoFaces& f, LoFaces& s, LoFaces& t){
    vector<LoFaces> pairs;
    for (LoFaces& i: product2(f, s)) {
        if (!conflict(i[0], i[1])) {
            pairs.push_back(i);
        }
    }
    vector<LoFaces> triples;
    for (LoFaces i: product3(pairs, t)) {
        if (verify_three( i ) ) {
            triples.push_back( i );
        }
    }
    int checks = f.size() * s.size() + pairs.size() * t.size();
    cout << triples.size() << " , " << checks << endl;
    return triples;
}



int main () {
    unordered_map< string, vector<NUM> > pruned_options;
    for (const string& loc: Locs){
        unordered_set<NUM> buffer;
        for (NUM& x: options[loc]){
            if (buffer.find(x) == buffer.end()){
                buffer.insert(x);
            }
        }
        pruned_options[loc] = vector<NUM> (buffer.begin(), buffer.end());
    }
    vv<NUM> pruned_vv;
    for (auto& key: Locs){
        pruned_vv.push_back(pruned_options[key]);
    }
    LoFaces good_faces = appendAll(pruned_vv);

    // Q2
    // NOTE: good_faces defined in Q1
    LoFaces A = copy_when(good_faces, 3);
    LoFaces B = copy_when(good_faces, 4);
    LoFaces C = copy_when(good_faces, 5);
    LoFaces D = copy_when(good_faces, 7);
    LoFaces E = copy_when(good_faces, 8);
    LoFaces F = copy_when(good_faces, 9);
   

    auto save = iter_three(A, B, C);
    cout << save.size() << endl;

    
    return 0;
}