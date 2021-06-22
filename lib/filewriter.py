def write(dictionary, file, missed):
    """A function that formats the input dictionary and writes it to the specified file.
    :param dictionary: A dictionary containing the equations.
    :param file: A string containing the location of the file to write to.
    :param missed: A string containing the location of the file to write unsolved equations to.
    """
    def get_keys_list(dic):
        """A function that puts all the keys of a dictionary in a list.
        :param dic: A dictionary containing the equations.
        :return: A list containing the keys of the input dictionary.
        """
        keys_list = []
        for key in dic.keys():
            keys_list.append(key)
        return keys_list

    def get_values_list(dic):
        """A function that puts all the values of a dictionary in a list.
        :param dic: A dictionary containing the equations.
        :return: A list containing the values of the input dictionary.
        """
        values_list = []
        for values in dic.values():
            values_list.append(values)
        return values_list

    num = 1
    index = 0
    list_with_keys = get_keys_list(dictionary)
    list_with_values = get_values_list(dictionary)
    missed_equations = dict()

    open(file, 'w')
    write_file = open(file, 'a')
    while index <= len(list_with_keys) - 1:
        if isinstance(list_with_values[index], list):
            missed_equations[index] = list_with_values[index]
        title = f"\n* {num} \nBOOL" + (" " * 4) + f"{str(list_with_keys[index])} = \n"
        equation = ("    " * 6) + f"({str(list_with_values[index])})"
        output = title + equation
        write_file.write(output)
        num = num + 1
        index = index + 1
    write_file.close()

    with open(missed, 'w') as file:
        for count, name in enumerate(missed_equations.keys(), start=0):
            if count == 0:
                file.write(f"{name}:\n")
            else:
                file.write(f"\n{name}:\n")
            file.write(f"\n".join(missed_equations[name]))
            file.write("\n")
