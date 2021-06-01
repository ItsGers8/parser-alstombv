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
            solvedEquationDict[key] = one_line_solver(dictionary[key], None, None)
    return solvedEquationDict


# Function that generates the correct string based on the syntax of the output file
def one_line_solver(equation, gates, variables):
    if variables is None:
        splitted_variables = equation[0].split("         ")[1]
        gates = get_gates(equation[1])
        variables = list(filter(None, splitted_variables.split(' ')))
    answer = " "
    for index, item in enumerate(gates, start=0):
        if item != "(R)" and item != "(T)":
            answer += gate_dict(index, item) + variables[index] + " "
    return answer


def gate_dict(index, gate):
    if index != 0:
        return {
            "] [": "* ",
            "]/[": "* .N."
        }[gate]
    else:
        return {
            "] [": "",
            "]/[": ".N."
        }[gate]


def large_equation_solver(equation):
    eq = Equation(equation[0].split(": ")[1].split(" ")[0], [])
    eq.add_path(Path(get_gates(equation[1]), get_names(equation[0])))
    print(eq)
    return equation


def get_gates(gates_in):
    return list(filter(None, re.findall('] \[|]/\[', gates_in)))


def get_names(names_in):
    return list(filter(None, re.split(' |Equation: [A-z]+', names_in)))


class Equation:
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths

    def add_path(self, path):
        self.paths.append(path)

    def __str__(self):
        response = "Equation " + self.name + ":"
        for path in self.paths[:-1]:
            response += "\n" + path.solve() + "+"
        response += "\n" + self.paths[-1].solve()
        return response


class Path:
    def __init__(self, gates, names):
        self.gates = gates
        self.names = names

    def solve(self):
        answer = " "
        for index, item in enumerate(self.gates, start=0):
            answer += gate_dict(index, item) + self.names[index] + " "
        return answer

    def __str__(self):
        response = ""
        for name in self.names[:-1]:
            response += name + ", "
        response += self.names[-1] + "\n"
        for gate in self.gates[:-1]:
            response += gate + ", "
        response += self.gates[-1]
        return response
