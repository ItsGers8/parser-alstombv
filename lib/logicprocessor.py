from lib.filereader import get_dict
import re

missed_count = 0


def get_dictionary(file):
    """A function that generates a dictionary with the equation name as key and the equation as value.
    :param file: A list with the lines of the file.
    :return: A dictionary with as a key the equation name and as a value the equation lines.
    """
    equation_dict = dict()
    for item in file:
        key = item[0].split(": ")[1].split(" ")[0]
        value = item[:-1]
        equation_dict[key] = value
    return equation_dict


def process(dictionary):
    """A function that processes the equations by checking their size and calling the corresponding function.
    :param dictionary: A dictionary with the equations.
    :return: A dictionary with as a key the name of the dictionary and as a value the solved version of that equation.
    """
    global missed_count
    solved_equation_dict = dict()
    for key in dictionary:
        if len(dictionary[key]) > 5:
            solved_equation_dict[key] = large_equation_solver(dictionary[key])
        elif len(dictionary[key]) == 5:
            solved_equation_dict[key] = medium_equation_solver(dictionary[key])
        else:
            solved_equation_dict[key] = small_equation_solver(dictionary[key], None, None)
    print(f"{len(dictionary)}   (total)\n"
          f"{missed_count}    (missed)\n"
          f"---- -\n{len(dictionary) - missed_count}   (done)\n"
          f"{round(100 - (missed_count / len(dictionary)) * 100, 2)}%  (done percentage)")
    return solved_equation_dict


# Function that generates the correct string based on the syntax of the output file
def small_equation_solver(equation, gates, variables):
    """A function that solves one lined equations by looking their gates up in the gate dictionary.
    :param equation: A list with the lines of the equation.
    :param gates: A list with all the gates of the equation, optional.
    :param variables: A list with all the gates of the equation, optional.
    :return: A string solution of the equation.
    """
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
    """A function that solves medium lined equations by combining all possible paths of the equation.
    :param equation: A list with the lines of the equation.
    :return: A string solution of the equation.
    """
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

    eq.add_path(Path(get_gates(equation[1]), get_names(equation[0])))

    for frag in frags:
        names_before = get_names(equation[0])[:len(get_gates(equation[1][:frag.start]))]
        names_path = get_names(equation[-2][frag.start:frag.end + 1])
        names_after = get_names(equation[0])[-len(get_gates(equation[1][frag.end:])) - 1:]
        names = names_before + names_path + names_after

        gates_before = get_gates(equation[1][:frag.start])
        gates_path = get_gates(equation[-1][frag.start:frag.end + 1])
        gates_after = get_gates(equation[1][frag.end:])
        gates = gates_before + gates_path + gates_after

        eq.add_path(Path(gates, names))
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
            eq.add_path(Path(gates, names))
    solution = f"{eq.paths[0].solve()}"
    for path in eq.paths[1:]:
        solution += f"+\n{ ' ' * 24 } {path.solve()}"
    return solution


def large_equation_solver(equation):
    """A function that is not yet implemented, but is used to track how many equations are not solved.
    :param equation: A list with the lines of the equation.
    :return: A string with the solution of the equation.
    """
    global missed_count
    missed_count += 1
    return equation


def gate_dict(index, gate) -> str:
    """A function that looks up what the input gate translates to in the filereader.get_dict() function.
    :param index: An int that tells what index this gate is in the list of gates of the equation.
    :param gate: A string containing the actual gate.
    :return: A string containing the translation of the gate.
    """
    position = "rest" if index != 0 else "start"
    return get_dict(position)[gate]


def get_gates(gates_in):
    """A function that strips all characters from a string, except for those part of a gate with a RegEx.
    :param gates_in: A string containing spaces, braces and backslashes.
    :return: A list of all the gates in the given string.
    """
    return list(filter(None, re.findall('] \\[|]/\\[', gates_in)))


def get_names(names_in):
    """A function that strips all characters from a string, except for those part of a gate name with a RegEx.
    :param names_in: A string containing spaces and characters.
    :return: A list of all the names in the given string.
    """
    return list(filter(None, re.split("Equation: [A-z\\-0-9]+ +| |\\|", names_in)))


class Equation:
    """A class used for keeping track of an equation."""
    def __init__(self, name):
        """A function that creates a new Equation.
        :param name: A string containing the name of the equation.
        """
        self.name = name
        self.paths = list()

    def add_path(self, path):
        """A function that adds a Path to the list of paths if it is not already in that list.
        :param path: A Path object.
        """
        if path not in self.paths:
            self.paths.append(path)

    def __str__(self):
        """A function that creates a string with the name of the equation and the solutions of its paths.
        :return: A string representation of the equation.
        """
        response = "Equation " + self.name + ":"
        for path in self.paths[:-1]:
            response += "\n" + path.solve() + "+"
        response += "\n" + self.paths[-1].solve()
        return response


class Path:
    """A class used for saving paths; routes from start to end in an equation."""
    def __init__(self, gates, names):
        """A function that creates a new path.
        :param gates: A list containing the gates of this path.
        :param names: A list containing the variable names of this path.
        """
        self.gates = gates
        self.names = names

    def solve(self):
        """A function that returns a string with the solution of the path by translating the gates.
        :return: A string containing the solution of the path.
        """
        answer = " "
        for index, item in enumerate(self.gates, start=0):
            answer += gate_dict(index, item) + self.names[index] + " "
        return answer

    def __str__(self) -> str:
        """A function that returns a string representation of the path.
        :return: A string containing the gates and the names of the gates.
        """
        return f"{self.gates} {self.names}"

    def __eq__(self, o: object) -> bool:
        """A function that checks if the input Path equals this Path.
        :param o: The comparing Path.
        :return: A bool that determines the equality of the objects.
        """
        return isinstance(o, Path) and self.solve() == o.solve()


class Fragment:
    """A class used for keeping track of Fragments of an equation; small possibilities of the equation."""
    def __init__(self, start, end, line):
        """A function that creates a new Fragment.
        :param start: An int determining where the Fragment started.
        :param end: An int determining where the Fragment ended.
        :param line: A string with the actual line of the Fragment.
        """
        self.start = start
        self.end = end
        self.line = line

    def __str__(self) -> str:
        """A function that returns a string representation of the Fragment.
        :return: A string containing the start, end and line variables.
        """
        return f"start: {self.start}, end: {self.end}\nline: {self.line}"

    def __eq__(self, o: object) -> bool:
        """A function that checks if the input Fragment equals this Fragment.
        :param o: The comparing Fragment.
        :return: A bool that determines the equality of the objects.
        """
        return isinstance(o, Fragment) and self.start == o.start and self.end == o.end and self.line == o.line
