import re


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
    splitted_variables = equation[0].split("         ")[1]
    gates = list(filter(None, re.split('[+-]', equation[1])))
    variables = list(filter(None, splitted_variables.split(' ')))
    answer = " "
    for index, item in enumerate(gates[:-1], start=0):
        answer += gate_dict(index, item) + variables[index] + " "
    return answer


def gate_dict(index, gate):
    if index != 0:
        return {
            "] [": "+ ",
            "]/[": "* .N."
        }[gate]
    else:
        return {
            "] [": "",
            "]/[": ".N."
        }[gate]


def large_equation_solver(equation):
    return equation
