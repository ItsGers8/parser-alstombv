def write(dictionary, file):
    def get_keys_list(dic):
        keys_list = []
        for key in dic.keys():
            keys_list.append(key)
        return keys_list

    def get_values_list(dic):
        values_list = []
        for values in dic.values():
            values_list.append(values)
        return values_list

    num = 1
    index = 0
    list_with_keys = get_keys_list(dictionary)
    list_with_values = get_values_list(dictionary)

    open(file, 'w')
    while index <= len(list_with_keys)-1:
        write_file = open(file, "a")

        res = '\n* {0} \n{1}    {2} = \n                        ({3})'.format(num, 'BOOL', str(list_with_keys[index]), str(list_with_values[index]))
        write_file.write(res)
        num = num + 1
        index = index + 1

        write_file.close()

# thisdict = {
#   "brand": "Ford",
#   "model": "Mustang",
#   "year": 1964
# }
# write(thisdict, "hopen.dat")