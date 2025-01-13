import numpy as np
import sys
from collections import defaultdict
import random

SIZE = 9
BLOCK_SIZE = 3

# Represent each cell in the board
class Variable:
    def __init__(self, row, col, value):
        self.row = row 
        self.col = col 
        self.value = value
        self.assigned = value != 0
        self.domain = {value} if self.assigned else set(range(1, 10))

    def __repr__(self):
        return f"Variable({self.row}, {self.col}, {self.domain})"

class KropkiSudokuCSP:
    def __init__(self, board, horizontal_dots, vertical_dots):
        self.variables = [[Variable(i, j, board[i][j]) for j in range(SIZE)] for i in range(SIZE)]
        self.horizontal_dots = horizontal_dots
        self.vertical_dots = vertical_dots
        self.constraints = defaultdict(set) # contain all variables with which var shares any constraints
        self.build_constraints()

    # define constraints for each variable based on Sudoku and Kropki constraints
    def build_constraints(self):
        for i in range(SIZE):
            for j in range(SIZE):
                var = self.variables[i][j]

                # Row and Column constraints
                for k in range(SIZE):
                    if k != j:
                        self.constraints[var].add(self.variables[i][k])
                    if k != i:
                        self.constraints[var].add(self.variables[k][j])

                # Block constraints
                block_row = (i // BLOCK_SIZE) * BLOCK_SIZE
                block_col = (j // BLOCK_SIZE) * BLOCK_SIZE
                for r in range(block_row, block_row + BLOCK_SIZE):
                    for c in range(block_col, block_col + BLOCK_SIZE):
                        if r != i or c != j:
                            self.constraints[var].add(self.variables[r][c])

                # Dot constraints
                # Horizontal neighbors
                if j < SIZE - 1:
                    neighbor = self.variables[i][j+1]
                    self.constraints[var].add(neighbor)

                if j > 0:
                    neighbor = self.variables[i][j-1]
                    self.constraints[var].add(neighbor)

                # Vertical neighbors
                if i < SIZE - 1:
                    neighbor = self.variables[i+1][j]
                    self.constraints[var].add(neighbor)

                if i > 0:
                    neighbor = self.variables[i-1][j]
                    self.constraints[var].add(neighbor)

    # check if the assignment is complete
    def is_complete(self):
        return all(var.assigned for row in self.variables for var in row)
    
    # select an unassigned variable using MRV and DH
    def select_unassigned_variable(self):
        # MRV heuristic
        unassigned_vars = [var for row in self.variables for var in row if not var.assigned]
        min_domain_size = min(len(var.domain) for var in unassigned_vars)
        mrv_vars = [var for var in unassigned_vars if len(var.domain) == min_domain_size]

        # if only one variable remains after MRV, return it
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        
        # apply DH to break ties
        max_degree = -1
        dh_vars = []
        for var in mrv_vars:
            degree = sum(1 for neighbor in self.constraints[var] if not neighbor.assigned)
            if degree > max_degree:
                max_degree = degree
                dh_vars = [var]
            elif degree == max_degree:
                dh_vars.append(var)
        
        # if only one variable remains after DH, return it
        if len(dh_vars) == 1:
            return dh_vars[0]

        # break ties randomly if needed
        return random.choice(dh_vars)
    
    # check if assigning value to var is consistent with all constraints.
    def is_consistent(self, var, value):
        i, j = var.row, var.col

        # Row and Column constraints
        for k in range(SIZE):
            # Alldiff(row)
            neighbor = self.variables[i][k]
            if neighbor != var and neighbor.assigned and value == neighbor.value:
                return False
            
             # Alldiff(col)
            neighbor = self.variables[k][j]
            if neighbor != var and neighbor.assigned and value == neighbor.value:
                return False
        
        # Block constraints
        # Alldiff(block)
        block_row = (i // BLOCK_SIZE) * BLOCK_SIZE
        block_col = (j // BLOCK_SIZE) * BLOCK_SIZE
        for r in range(block_row, block_row + BLOCK_SIZE):
            for c in range(block_col, block_col + BLOCK_SIZE):
                neighbor = self.variables[r][c]
                if neighbor != var and neighbor.assigned and value == neighbor.value:
                    return False
        
        # Horizontal constraints
        # right neighbor
        if j < SIZE - 1:
            neighbor = self.variables[i][j+1]
            dot = self.horizontal_dots[i][j]
            if dot != 0:
                if neighbor.assigned:
                    if not self.dot_constraints(value, neighbor.value, dot):
                        return False
                else:
                    # enforce dot constraints on neighbor's domain
                    possible_values = set()
                    for neighbor_value in neighbor.domain:
                        if self.dot_constraints(value, neighbor_value, dot):
                            possible_values.add(neighbor_value)
                    # if no values are possible for neighbor, this assignment is not consisitent
                    if not possible_values:
                        return False
        
        # left neighbor
        if j > 0:
            neighbor = self.variables[i][j-1]
            dot = self.horizontal_dots[i][j-1]
            if dot != 0:
                if neighbor.assigned:
                    if not self.dot_constraints(value, neighbor.value, dot):
                        return False
                else:
                    # enforce dot constraints on neighbor's domain
                    possible_values = set()
                    for neighbor_value in neighbor.domain:
                        if self.dot_constraints(value, neighbor_value, dot):
                            possible_values.add(neighbor_value)
                    # if no values are possible for neighbor, this assignment is not consisitent
                    if not possible_values:
                        return False
                    
        # Vertical constraints
        # down neighbor
        if i < SIZE - 1:
            neighbor = self.variables[i+1][j]
            dot = self.vertical_dots[i][j]
            if dot != 0:
                if neighbor.assigned:
                    if not self.dot_constraints(value, neighbor.value, dot):
                        return False
                else:
                    # enforce dot constraints on neighbor's domain
                    possible_values = set()
                    for neighbor_value in neighbor.domain:
                        if self.dot_constraints(value, neighbor_value, dot):
                            possible_values.add(neighbor_value)
                    # if no values are possible for neighbor, this assignment is not consisitent
                    if not possible_values:
                        return False
                    
        # up neighbor
        if i > 0:
            neighbor = self.variables[i-1][j]
            dot = self.vertical_dots[i-1][j]
            if dot != 0:
                if neighbor.assigned:
                    if not self.dot_constraints(value, neighbor.value, dot):
                        return False
                else:
                    # enforce dot constraints on neighbor's domain
                    possible_values = set()
                    for neighbor_value in neighbor.domain:
                        if self.dot_constraints(value, neighbor_value, dot):
                            possible_values.add(neighbor_value)
                    # if no values are possible for neighbor, this assignment is not consisitent
                    if not possible_values:
                        return False
                    
        return True
    
    def dot_constraints(self, value1, value2, dot):
        # 0: no dot; 1: white; 2: black
        if dot == 1:
            return abs(value1 - value2) == 1
        elif dot == 2:
            return value1 == value2 * 2 or value2 == value1 * 2
        else:
            return True
            
    def order_domain_values(self, var):
        return sorted(var.domain)
    
    def assign(self, var, value):
        var.domain = {value}
        var.assigned = True
        var.value = value

    def unassign(self, var, domain):
        var.domain = domain
        var.assigned = False
        var.value = None

class KropkiSudokuSolver:
    def __init__(self, csp):
        self.csp = csp

    def backtrack_search(self):
        return self.backtrack()
    
    def backtrack(self):
        if self.csp.is_complete():
            return True
        
        var = self.csp.select_unassigned_variable()
        original_domain = var.domain.copy()

        for value in self.csp.order_domain_values(var):
            if self.csp.is_consistent(var, value):
                self.csp.assign(var, value)
                inferences = {}
                if self.inference(var, value, inferences):
                    result = self.backtrack()
                    if result:
                        return True
                    
                # Revert inferences
                self.restore_inferences(inferences)

                # Revert the domain to what it was before the assignment
                self.csp.unassign(var, original_domain)
            else:
                continue

        self.csp.unassign(var, original_domain)
        return False
    
    # Extra Credit
    def inference(self, var, value, inferences):
        # Forward Checking
        for neighbor in self.csp.constraints[var]:
            if not neighbor.assigned:
                if value in neighbor.domain:
                    # Remove value due to Alldiff constraints
                    neighbor.domain.remove(value)
                    # Record inference
                    if neighbor not in inferences:
                        inferences[neighbor] = set()
                    inferences[neighbor].add(value)

                    if len(neighbor.domain) == 0:
                        return False
                    
                # dot constraints
                dot = self.get_dot(var, neighbor)
                if dot != -1:
                    # Remove inconsistent values from neighbor's domain
                    inconsistent_values = set()
                    for neighbor_value in neighbor.domain:
                        if not self.csp.dot_constraints(value, neighbor_value, dot):
                            inconsistent_values.add(neighbor_value)
                    
                    if inconsistent_values:
                        neighbor.domain -= inconsistent_values
                        if neighbor not in inferences:
                            inferences[neighbor] = set()
                        inferences[neighbor] |= inconsistent_values

                    if len(neighbor.domain) == 0:
                        return False
        return True
    
    def restore_inferences(self, inferences):
        for var, removed_values in inferences.items():
            var.domain |= removed_values
                
    def get_dot(self, var1, var2):
        row1, col1 = var1.row, var1.col
        row2, col2 = var2.row, var2.col

        # Horizontal dot
        if row1 == row2:
            if col1 + 1 == col2:
                return self.csp.horizontal_dots[row1][col1]
            elif col1 == col2 + 1:
                return self.csp.horizontal_dots[row1][col2]
        # Vertical dot
        elif col1 == col2:
            if row1 + 1 == row2:
                return self.csp.vertical_dots[row1][col1]
            elif row1 == row2 + 1:
                return self.csp.vertical_dots[row2][col1]
            
        return -1 # Not neighbors


def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_file output_file")
        sys.exit(1)

    input = sys.argv[1]
    output = sys.argv[2]
    
    # read input
    with open(input, 'r') as file:
        lines = file.readlines()
    board = [[int(x) for x in lines[i].split()] for i in range(9)]
    horizontal_dots = [[int(x) for x in lines[10 + i].split()] for i in range(9)]
    vertical_dots = [[int(x) for x in lines[20 + i].split()] for i in range(8)]

    csp = KropkiSudokuCSP(board, horizontal_dots, vertical_dots)
    solver = KropkiSudokuSolver(csp)

    if solver.backtrack_search():
        # write output
        with open(output, 'w') as f:
            for row in csp.variables:
                f.write(' '.join(str(var.value) for var in row) + '\n')
        print("Solution written to", output)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()