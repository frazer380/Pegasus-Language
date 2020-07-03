# IMPORTS
import sys
from ast import literal_eval

# VARIABLE DECLARATIONS
variables = []
arrays = []
file = ""
filename = ""
forFlag = 0

def error(filename, line, text, message):
    line = line + 1
    print("File \"" + filename + "\", " + str(line))
    print(text)
    print(message)

def interpret(line, number):
    if line.endswith(";"):
        if line.startswith("//"):
            pass
        if line.startswith("print"):
            new_line_contents = line.replace("print", "").strip()
            if new_line_contents.startswith("\""):
                if new_line_contents.endswith("\";"):
                    string = new_line_contents[1:]
                    string = string[:-2]
                    print(string)
            elif new_line_contents.startswith("arr:"):
                new_line_contents = new_line_contents.replace("arr:", "").strip()
                new_line_contents = new_line_contents[:-1]
                varName = new_line_contents.split("[", 1)[0]
                new_line_contents = new_line_contents.split(varName, 1)[1]
                empty = True
                index = 0
                if new_line_contents != "":
                    empty = False
                    new_line_contents = new_line_contents.replace("[", "").strip()
                    new_line_contents = new_line_contents.replace("]", "").strip()
                    index = new_line_contents
                for i in arrays:
                    for j in i:
                        if varName in j:
                            newArr = i[1:]
                            if empty == True:
                                print(newArr)
                            elif empty == False:
                                print(newArr[int(index)])
                            
            else:
                final_line_contents = new_line_contents.replace("var", "").strip()
                varListLength = len(variables)
                if varListLength > 0:
                    for i in range(varListLength):
                        var = variables[i]
                        var2 = "".join(str(e) for e in var)
                        final_line_contents = final_line_contents[:-1]
                        if final_line_contents in var2:
                            print(var2.replace(final_line_contents, "").strip())
                else:
                    error(filename, number, line, "Variable \"" + final_line_contents.replace(";", "") + "\" does not exist")
        if line.startswith("var"):
            new_line_contents = line.replace("var", "").strip()
            variableName = new_line_contents.split("=", 1)[0]
            value = new_line_contents.split("=", 1)[1]
            if value.strip().startswith("["):
                value = value[:-1].strip()
                value = literal_eval(value)
                value.insert(0, variableName)
                arrays.append(value)
            else:
                value = value[:-1]
                variables.append([variableName, value])
        if line.startswith("for"):
            new_line_contents = line.replace("for", "").strip()
            variableName = new_line_contents.split("in", 1)[0]
            ranges = new_line_contents.split("in", 1)[1]
            x = ranges.split()
            for variableName in range(int(x[0]), int(x[1])):
                forFlag = 1
    elif line.endswith(";") != True:
        if line.strip():
            error(filename, number, line, "Semicolon missing")
    elif line.startswith(""):
        pass

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
        setup(file)
    except:
        print("File does not exist or one isn't specified!")

if __name__ == '__main__':
    main()