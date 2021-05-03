# Function that generates a dictionary with equation name as key and the equation as the value
def get_dictionary(file):
    equationDict = dict()
    for item in file:
        equationDict[item[0].split(": ")[1].split(" ")[0]] = item[1:-1]
    return equationDict


# Function that processes the equations by checking what size they are and calling the according function
def process(dictionary):
    return dictionary


# Function that generates the correct string based on the syntax of the output file
def one_line_solver(equation):
    return equation
