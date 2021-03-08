def getData(source):
    with open(source) as file:
        fileData = file.read()

    return fileData.replace("\n\n", "").splitlines()[5:]


def stripData(inp):
    strip = list()
    for element in inp:
        strip.append(element[5:])
    return strip


def seperateEquations(strip):
    equations = list()
    for element in strip:
        if "Equation" in element:
            equations.append([element])
        elif "EQUATION INDEX" in element:
            break
        else:
            equations[-1].append(element)
    return equations


def putEquationInString(inputList):
    equationsTogether = list()
    for element in inputList:
        for index, line in enumerate(element, start=0):
            if index == 0:
                equationsTogether.append(line.replace("         ", " "))
            else:
                equationsTogether[-1] += "\n" + line


def createEquationDictionary(inputEquations):
    equationDict = dict()
    for item in inputEquations:
        equationDict[item[0].split(": ")[1].split(" ")[0]] = item[0:]
    return equationDict


def checkIfFinalIsKey(inp, equationDict):
    counter = 0
    for number, val in enumerate(inp, start=1):
        if equationDict[val][0].split(": ")[1].replace("         ", " ").split(" ")[1:][-1] != key:
            continue
        else:
            counter += 1
    return counter == len(equationDict)


def removeEmptyListItems(inputList):
    returnList = list()
    for element in inputList:
        if element != "":
            returnList.append(element)
    return returnList


def dictionarify(val):
    newDict = dict()
    keys = removeEmptyListItems(val[0].split(": ")[1].replace("         ", " ").split(" ")[1:])
    for number, entry in enumerate(removeEmptyListItems(val[1].replace("+", "").split("-")), start=0):
        newDict[keys[number]] = entry
    return newDict


def solve(solveDict):
    theString = ""
    for number, entry in enumerate(solveDict):
        if number + 1 == len(solveDict):
            theString = entry + " = " + theString
        else:
            if solveDict[entry] == "] [":
                if number == 0:
                    theString += "(" + entry + ")"
                else:
                    theString += ".(" + entry + ")"
            elif solveDict[entry] == "]/[":
                theString += "¬(" + entry + ")"
            else:
                continue
    return theString


data = getData("resources/input.txt")
stripped = stripData(data)
sepEquations = seperateEquations(stripped)
eqDict = createEquationDictionary(sepEquations)

count = 0
for key in eqDict:
    value = eqDict[key]
    if len(value) == 3:
        count += 1
        dictionary = dictionarify(value)
        answer = solve(dictionary)
        print(count, answer)

print(len(eqDict))
