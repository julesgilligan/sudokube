#pragma once

#include <iostream>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <array>
#include <list>
#include <vector>

using namespace std;
typedef int NUM;
typedef vector<NUM> Face;
typedef vector<Face> LoFaces;

template <class T>
using vv = vector<vector<T>>;

extern const vv<NUM> allowed_doubles; // forward dec

template <class T>
ostream& operator<<(ostream& os, const vector<T>& v)
{
    bool first = true;
    for (T const& it : v)
    {
        if (first == true) {
            os << "[";
            first = false;
        } else {
            os << ", ";
        }
        os << it;
    }
    os << "]";
    return os;
}

ostream& operator<<(ostream& os, const unordered_map<string, vector<NUM>>& um)
{
    bool first = true;
    for (auto const& it : um)
    {
        if (first != true) {
            os << endl;
        }
        os << it.first    // string (key)
            << ':'
            << it.second;   // print vector
         first = false;
    }
    return os;
}

bool aNotInB(NUM& A, Face B) {
    std::vector<NUM>::iterator it;
    it = find (B.begin(), B.end(), A);
    return (it == B.end());
}


vector<LoFaces> product2(LoFaces& A, LoFaces& B){
    vector<LoFaces> ret;
    for (Face& x: A){
        for (Face& y: B) {
            ret.push_back(LoFaces{x,y});
        }
    }
    return ret;
}

vector<LoFaces> product3(vector<LoFaces>& A, LoFaces& B){
    vector<LoFaces> ret;
    for (LoFaces x: A){
        for (auto& y: B){
            x.push_back(y);
            ret.push_back(x);
            x.pop_back();
        }
    }
    return ret;
}

bool conflict(Face& f1, Face& f2){
    for (NUM i = 0; i < 9; ++i) {
        if (i == 1) continue;
        if (f1[i] == f2[i]){
            if (aNotInB(f1[i], allowed_doubles[i]))
                return true;
        } 
    }
    return false;
}

//Verify Three running too long Mar 7
bool verify_three(LoFaces LoF) {
    Face a = LoF[0];
    Face b = LoF[1];
    Face c = LoF[2];
    for (NUM i = 0; i < 9; ++i) { 
        if (i == 1) continue;  // 1 is guaranteed to be fine
        if ((c[i] == a[i]) || (c[i] == b[i])){
            if (aNotInB(c[i], allowed_doubles[i]))
                return false;
            if (a[i] == b[i])
                return false;
        }
        // Slows down verify(), but still faster than an extra conflict()
        /*if (a[i] == b[i]) {
            if (aNotInB(a[i], allowed_doubles[i])){
                return false;
            }
        }*/
    }
    return true;
}