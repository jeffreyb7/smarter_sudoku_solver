import math

class Constraint:

    def __init__(self, variable):
        self.variable = variable

    def satisfied(self, assignment):
        pass

class ColumnConstraint(Constraint):

    def __init__(self, variable):
        super().__init__(variable)
    
    def satisfied(self, assignment):
        # Get col number of var
        var_col = self.variable % 9
        # List all vars in column
        var_to_check = [x for x in range(var_col, 81, 9)]
        var_values = []
        # Check that none of these vars have same assignment
        for variable in var_to_check:
            if variable in assignment:
                if assignment[variable] in var_values:
                    return False
                else:
                    var_values.append(assignment[variable])
            else:
                continue

        return True

class RowConstraint(Constraint):

    def __init__(self, variable):
        super().__init__(variable)
    
    def satisfied(self, assignment):
        # Get row number of var
        var_row = math.floor(self.variable / 9)
        # List all vars in row
        var_to_check = [x for x in range(var_row*9, ((var_row+1)*9))]
        var_values = []
        # Check that none of these vars have same assignment
        for variable in var_to_check:
            if variable in assignment:
                if assignment[variable] in var_values:
                    return False
                else:
                    var_values.append(assignment[variable])
            else:
                continue

        return True


class SectorConstraint(Constraint):
 
    def __init__(self, variable):
        super().__init__(variable)
    
    def satisfied(self, assignment):
        # Get row, col indices of variable
        row_idx = math.floor(self.variable / 9)
        col_idx = self.variable % 9
        # Get sector number of var
        # Sectors are numbered 0 to 8 
        # Sector 0 is top left
        # Sector 2 is top right
        # Sector 6 is bottom left
        # Sector 8 is bottom right
        sector_idx = (math.floor(row_idx / 3) * 3) + math.floor(col_idx / 3)
        # Get lowest var number in sector
        lowest_var_id = (math.floor(sector_idx / 3) * 27) + ((sector_idx % 3) * 3)
        # Produce list of all vars in sector, starting with first 3
        base_var_to_check = [x for x in range(lowest_var_id, lowest_var_id+3)]
        final_var_to_check = []
        # Add remaining vars in sector
        for entry in base_var_to_check:
            final_var_to_check.append(entry)
            final_var_to_check.append(entry + 9)
            final_var_to_check.append(entry + 18)
        # Check that none of these vars have same assignment
        var_values = []
        for variable in final_var_to_check:
            if variable in assignment:
                if assignment[variable] in var_values:
                    return False
                else:
                    var_values.append(assignment[variable])
            else:
                continue

        return True



class CSP:

    def __init__(self, variables, domains):

        self.variables = variables
        self.domains = domains
        self.constraints = {}

        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it")

    def add_constraint(self, constraint):

        if constraint.variable not in self.variables:
            raise LookupError("Variable in constraint not in CSP")
        else:
            self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True


    def backtracking_search(self, assignment):
        # Check if each variable has an assignment. If so, stop
        if len(assignment) == len(self.variables):
            return assignment

        # Get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # Get every possible domain value of the first unassigned variable
        first_var = unassigned[0]
        for value in self.domains[first_var]:
            local_assignment = assignment.copy()
            local_assignment[first_var] = value
            # Check if constraints are satisfied.
            # If so, continue to recurse
            if self.consistent(first_var, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None

        
if __name__ == "__main__":
    
    puzzle_design = [
            [3, 0, 4, 0, 2, 0, 0, 6, 5],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 9, 8, 0, 0, 1],
            [0, 0, 8, 9, 6, 2, 3, 0, 0],
            [6, 0, 9, 1, 0, 7, 2, 0, 4],
            [0, 0, 7, 5, 3, 4, 6, 0, 0],
            [9, 0, 0, 8, 1, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 9],
            [4, 5, 0, 0, 7, 0, 8, 0, 6]
            ]

    # Initialize variables and domains
    # Variable ids are just numbers from 0 to 80
    # Var 0 is upper left of puzzle
    # Var 80 is bottom right of puzzle
    variables = [x for x in range(0, 81)]
    # Create domains for each variable
    domains = {}
    for variable in variables:
        domains[variable] = [x for x in range(1, 10)]

    # Create initial assignment dictionary
    # This maps variable to value for the initial state of the puzzle
    assignment = {}
    variable_id = 0
    for row_idx in range(0, 9):
        for col_idx in range(0, 9):
            if puzzle_design[row_idx][col_idx] != 0:
                assignment[variable_id] = puzzle_design[row_idx][col_idx]
                variable_id += 1
            else:
                variable_id += 1
    
    # Instantiate CSP class
    csp = CSP(variables, domains)

    # Add constraints
    for variable in variables:
        csp.add_constraint(RowConstraint(variable))
        csp.add_constraint(ColumnConstraint(variable))
        csp.add_constraint(SectorConstraint(variable))

    # Get solution
    solution = csp.backtracking_search(assignment)
    if solution is None:
        print('No solution found')
    else:
        # Sort dictionary in ascending order
        solution_keys_sorted = sorted(solution.keys())
        ordered_solution = {}
        for key in solution_keys_sorted:
            ordered_solution[key] = solution[key]
        print(ordered_solution)
        solution_array = []
        row_array = []
        for key, value in ordered_solution.items():
            if (key + 1) % 9 == 0:
                row_array.append(value)
                solution_array.append(row_array)
                row_array = []
            else:
                row_array.append(value)
        for row in solution_array:
            for element in row:
                print(element, end = ' ')
            print()



            
