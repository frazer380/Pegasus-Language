# IMPORTS
import sys
from interpret import *

def setup(filename):
    read_lines = filename.readlines()
    read_lines_stripped = [line.strip("\n") for line in read_lines]
    read_lines_enum = enumerate(read_lines_stripped)
    for count, item in read_lines_enum:
        interpret(item, count)

def main():
    global file
    global filename
    try:
        file = open(sys.argv[1])
        filename = sys.argv[1]
        setFilename(filename)
        setup(file)
    except OSError:
        print("File does not exist or one isn't specified!")

if __name__ == '__main__':
    main()