from lib.filereader import get_dict
import re

missed_count = 0


# Function that generates a dictionary with equation name as key and the equation as the value
def get_dictionary(file):
    equation_dict = dict()
    for item in file:
        key = item[0].split(": ")[1].split(" ")[0]
        value = item[:-1]
        equation_dict[key] = value
    return equation_dict


# Function that processes the equations by checking what size they are and calling the according function
def process(dictionary):
    global missed_count
    solved_equation_dict = dict()
    for key in dictionary:
        if len(dictionary[key]) > 5:
            solved_equation_dict[key] = large_equation_solver(dictionary[key])
        elif len(dictionary[key]) == 5:
            solved_equation_dict[key] = medium_equation_solver(dictionary[key])
        else:
            solved_equation_dict[key] = one_line_solver(dictionary[key], None, None)
    print(f"{len(dictionary)}   (total)\n"
          f"{missed_count}    (missed)\n"
          f"---- -\n{len(dictionary) - missed_count}   (done)\n"
          f"{round(100 - (missed_count / len(dictionary)) * 100, 2)}%  (done percentage)")
    return solved_equation_dict


# Function that generates the correct string based on the syntax of the output file
def one_line_solver(equation, gates, variables):
    if variables is None:
        split_variables = equation[0].split("         ")[1]
        gates = get_gates(equation[1])
        variables = list(filter(None, split_variables.split(' ')))
    answer = " "
    for index, item in enumerate(gates, start=0):
        if item != "(R)" and item != "(T)":
            answer += gate_dict(index, item) + variables[index] + " "
    return answer


def medium_equation_solver(equation):
    eq = Equation(equation[0].split(": ")[1].split(" ")[0])
    paths = []
    frags = []
    for index, char in enumerate(equation[-1], start=0):
        if char == "+" and equation[-2][index] == "|" and \
                (index == (len(equation[-1]) - 1) or equation[-1][index + 1] != " "):
            for index2, _ in enumerate(equation[-1], start=0):
                if index2 <= index:
                    continue
                if index2 + 1 == len(equation[-1]):
                    paths.append([index, index2])
                elif equation[-2][index2] == "|" and equation[-1][index2] in "+|":
                    paths.append([index, index2])
                    if equation[-1][index2 + 1] == " ":
                        break
    for num in paths:
        frags.append(Fragment(num[0], num[1], equation[-1]))

    eq.add_path(Path(get_gates(equation[1]), get_names(equation[0]), 0, len(equation[1])))

    for frag in frags:
        names_before = get_names(equation[0])[:len(get_gates(equation[1][:frag.start]))]
        names_path = get_names(equation[-2][frag.start:frag.end + 1])
        names_after = get_names(equation[0])[-len(get_gates(equation[1][frag.end:])) - 1:]
        names = names_before + names_path + names_after

        gates_before = get_gates(equation[1][:frag.start])
        gates_path = get_gates(equation[-1][frag.start:frag.end + 1])
        gates_after = get_gates(equation[1][frag.end:])
        gates = gates_before + gates_path + gates_after

        eq.add_path(Path(gates, names, frags[0].start, frags[0].end))
        for index2, frag2 in enumerate(frags, start=0):
            if frag2 == frag or frag2.start < frag.end:
                continue
            equation[0] = re.split("Equation: [A-z\\-0-9]+ {5}", equation[0])[-1]
            between_names = get_names(equation[0][frag.end:frag2.start])
            path2_names = get_names(equation[-2][frag2.start:frag2.end + 1])
            after_names = get_names(equation[0][frag2.end:])
            names = names_before + names_path + between_names + path2_names + after_names

            gates_between = get_gates(equation[1][frag.end:frag2.start])
            gates_path2 = get_gates(equation[-1][frag2.start:frag2.end + 1])
            gates_after = get_gates(equation[1][frag2.end:])
            gates = gates_before + gates_path + gates_between + gates_path2 + gates_after
            eq.add_path(Path(gates, names, 0, len(equation[1])))
    solution = f"{eq.paths[0].solve()}"
    for path in eq.paths[1:]:
        solution += f"+\n\t\t\t\t\t\t {path.solve()}"
    return solution


def large_equation_solver(equation):
    global missed_count
    missed_count += 1
    return equation


def gate_dict(index, gate):
    position = "rest" if index != 0 else "start"
    return get_dict(position)[gate]


def get_gates(gates_in):
    return list(filter(None, re.findall('] \\[|]/\\[', gates_in)))


def get_names(names_in):
    return list(filter(None, re.split("Equation: [A-z\\-0-9]+ +| |\\|", names_in)))


class Equation:
    def __init__(self, name):
        self.name = name
        self.paths = list()

    def add_path(self, path):
        if path not in self.paths:
            self.paths.append(path)

    def __str__(self):
        response = "Equation " + self.name + ":"
        for path in self.paths[:-1]:
            response += "\n" + path.solve() + "+"
        response += "\n" + self.paths[-1].solve()
        return response


class Path:
    def __init__(self, gates, names, start, end):
        self.gates = gates
        self.names = names
        self.start = start
        self.end = end

    def solve(self):
        answer = " "
        for index, item in enumerate(self.gates, start=0):
            answer += gate_dict(index, item) + self.names[index] + " "
        return answer

    def __str__(self) -> str:
        return f"{self.gates} {self.names} {self.start} {self.end}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Path) and self.solve() == o.solve()


class Fragment:
    def __init__(self, start, end, line):
        self.start = start
        self.end = end
        self.line = line

    def __str__(self) -> str:
        return f"start: {self.start}, end: {self.end}\nline: {self.line}"

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Fragment) and self.start == o.start and self.end == o.end and self.line == o.line
