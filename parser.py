import lib.filereader as reader
import lib.filewriter as writer
import lib.logicprocessor as processor

if __name__ == "__main__":
    file = reader.get_file('resources/input.txt')
    for item in file:
        for element in item:
            print(element)


