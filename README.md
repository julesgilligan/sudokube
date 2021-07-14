# Sudokube
A cute mash up of "sudoku cube" that sounds like "psuedo cube". This is a mini exploration of a Rubik's Cube with sudoku faces.

The first time I picked up the toy I solved it with pencil and paper in about half an hour. How carefully designed was this toy to be
solved at this difficulty? What kind of information can you drop to keep a single solution?

I wanted to know what different levels of constraints added to the solution of this little toy. I started with the Python script
that checks how many possible cubes could be solved from a naive approach. Then, little by little I incorporate in more constraints 
from the toy (such as the required locations each number) to limit the possible solutions. 

When I was satisfied with that answer I tried to write the same algorithm in C++ because I've heard it's whippin' fast. That was quickly
abandoned when the first couple steps ran in either comperable or greater time (and writing C++ isn't as enjoyable as Python)
