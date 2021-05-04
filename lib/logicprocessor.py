# Function that generates a dictionary with equation name as key and the equation as the value
def get_dictionary(file):
    equationDict = dict()
    for item in file:
        key = item[0].split(": ")[1].split(" ")[0]
        value = item[:-1]
        equationDict[key] = value
    return equationDict


# Function that processes the equations by checking what size they are and calling the according function
def process(dictionary):
    solvedEquationDict = dict()
    for key in dictionary:
        if len(dictionary[key]) > 2:
            solvedEquationDict[key] = large_equation_solver(dictionary[key])
        else:
            solvedEquationDict[key] = one_line_solver(dictionary[key])
    return solvedEquationDict


# Function that generates the correct string based on the syntax of the output file
def one_line_solver(equation):
    return equation


def large_equation_solver(equation):
    return equation
