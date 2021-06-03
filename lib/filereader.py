import json


def get_file(location):
    with open(location) as file:
        file_data = file.read()
    output = strip_data(file_data.replace("\n\n", "").splitlines()[5:])
    return separate_equations(output)


def strip_data(inp):
    strip = list()
    for element in inp:
        strip.append(element[5:])
    return strip


def separate_equations(strip):
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
    return json.load(open("resources/GateLibrary.json"))[position]
