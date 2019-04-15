This is a submission by Kenrick Tse (kt1556) for Lab 3 of Operating Systems, CSCI 202, Fall 2018.

The source code for the lab is all contained in one file, bankers.py. 

However, the program requires your selected input text file to be in the same directory.

I have included in the .zip the input files provided on the website, for the convenience of the grader. These have not been modified.

The version used is Python 3.7, and requires no external libraries (though it uses sys and copy, which are part of the standard library).

=================================================================================

Compiling and Running:

While in the directory of the file, type in command prompt:
python bankers.py <input-filename>

The output should be printed to the screen straight away. For example, using input-01.txt:
python bankers.py input-01.txt

Should yield the following output:

FIFO
==========
Task 1  3   0   0%
Task 2  3   0   0%
Total   6   0   0%


BANKER'S
==========
Task 1  3   0   0%
Task 2  5   2   40%
Total   8   2   25%