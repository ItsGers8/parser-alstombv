import json


def get_file(location):
    """A function that reads the specified file and removes blank lines.
    :param location: A string containing the location of the file to read.
    :return: A list containing all the lines of the file.
    """
    with open(location) as file:
        file_data = file.read()
    output = strip_data(file_data.replace("\n\n", "").splitlines()[5:])
    return separate_equations(output)


def strip_data(inp):
    """A function that removes the first five spaces in the file.
    :param inp: An input list of strings.
    :return: A list containing all the lines of the file, without the indentation at the front of each line.
    """
    strip = list()
    for element in inp:
        strip.append(element[5:])
    return strip


def separate_equations(strip):
    """A function that separates the equations from a list filled with strings to a list with lists of equations.
    :param strip: An input list containing all the lines of the equation.
    :return: A list containing lists of equations.
    """
    equations = list()
    for element in strip:
        if "Equation" in element:
            equations.append([element])
        elif "EQUATION INDEX" in element:
            break
        else:
            equations[-1].append(element)
    return equations


def get_dict(position):
    """A function that loads the dictionary in resources/GateLibrary.json to see to what which gate translates.
    :param position: A string containing whether or not the gate is the first or last gate.
    :return: The correct dictionary according to the position.
    """
    return json.load(open("resources/GateLibrary.json"))[position]
