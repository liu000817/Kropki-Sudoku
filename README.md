# Kropki-Sudoku
# How to run
```
python sudoku.py <input_file> <output_file>
```

# Project Description: 
Implement the Backtracking Algorithm to solve the Kropki Sudoku puzzle. The rules of the game are:<br />
• The game board consists of 9 × 9 cells divided into 3 × 3 non-overlapping blocks as shown below. Some of the cells already have digits (1 to 9) assigned to them initially.<br />
• The goal is to find assignments (1 to 9) for the empty cells so that every row, every column, and every 3x3 block contains the digits from 1 to 9 exactly once.<br />
• A white dot between two adjacent cells requires that the value in one cell is exactly 1 greater than the value of the other cell. This could be satisfied in either direction; e.g., “3 & 4” or “4 & 3” will both satisfy the requirement. A black dot between two adjacent cells requires that the value in one cell is exactly double the value of the other cell. This also could be satisfied in either direction; e.g., “3 & 6” or “6 & 3.” If there is no dot between two adjacent cells, then neither condition needs to be fulfilled between the two cells.

In the Backtracking Algorithm, use the minimum remaining value and degree heuristics to implement the SELECT-UNASSIGNED-VARIABLE function. For the ORDER-DOMAIN-VALUES function, simply order the domain values in increasing order from 1 to 9 instead of using heuristics. You can skip the INFERENCE function inside the Backtracking Algorithm in your implementation.

# Input and output formats: 
The program will read in the initial game board values from an input text file and then produce an output text file that contains the solution. 

The format of the input file is as follows: The first 9 rows contain the initial cell values of the game board, separated by blanks. The cell values range from 0 to 9, with 0 indicating a blank cell. This is followed by a blank line. The next 9 rows contain the locations of dots between horizontally-adjacent cells. Row #1 contains the locations of dots for horizontally-adjacent cells in row #1 of the game board, and similarly for the other rows. A value of 0 means there is no dot between two adjacent cells, a value of 1 means there is a white dot between two adjacent cells, and a value of 2 means there is a black dot between two adjacent cells. This is then followed by another blank line. The next 8 rows contain the locations of dots between vertically-adjacent cells. Row #1 contains the locations of dots between vertically-adjacent cells in the first and second rows of the game board, and similarly for the other rows. Again, a value of 0 means there is no dot between two adjacent cells, a value of 1 means there is a white dot between two adjacent cells, and a value of 2 means there is a black dot
between two adjacent cells. 

The format of the output file is as follows: The output file contains 9 rows of integers ranging from 1 to 9, separated by blanks.