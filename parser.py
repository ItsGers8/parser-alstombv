import lib.filereader as reader
import lib.filewriter as writer
import lib.logicprocessor as processor

if __name__ == "__main__":
    file = reader.get_file('resources/input.txt')
    dictionary = processor.get_dictionary(file)
    output = processor.process(dictionary)
    writer.write(output, 'resources/output.dat')
