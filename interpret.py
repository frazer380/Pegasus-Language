import sys
from ast import literal_eval
from error import *

sys.setrecursionlimit(5000)

# VARIABLE DECLARATIONS
variables = []
arrays = []
filename = ""

elseFlag = 0

def setFilename(fileParam):
    global filename
    filename = fileParam

def interpret(line, number):
    global elseFlag
    if line.endswith(";") or line.endswith("{") or line.endswith("}"):
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
            elif new_line_contents.startswith("var:"):
                final_line_contents = new_line_contents.replace("var:", "")[:-1]
                for i in range(0, len(variables)):
                    if final_line_contents in variables[i][0]:
                        print(variables[i][1].strip())
                
        if line.startswith("var"):
            new_line_contents = line.replace("var", "").strip()
            variableName = new_line_contents.split("=", 1)[0]
            value = new_line_contents.split("=", 1)[1]
            if value.strip() == "input();":
                userInput = input()
                variables.append([variableName, userInput])
            else:
                if value.strip().startswith("["):
                    value = value[:-1].strip()
                    value = literal_eval(value)
                    value.insert(0, variableName)
                    arrays.append(value)
                else:
                    value = value[:-1]
                    variables.append([variableName, value])
        if line.startswith("if"):
            new_line_contents = line.replace("if", "")
            variableName =  new_line_contents.split("==", 1)[0].strip()
            new_line_contents = new_line_contents.replace(variableName, "").strip()
            new_line_contents = new_line_contents.replace("==", "").strip()
            value = new_line_contents.split(":", 1)[0]
            varListLength = len(variables)
            for i in range(varListLength):
                var = variables[i]
                var2 = "".join(str(e) for e in var)
                if variableName in var2:
                    var2 = var2.replace(variableName, "").split()
                    if value == var2[0]:
                        new_line_contents = line.split(":", 1)[1].strip()
                        interpret(new_line_contents, 0)
                    else:
                        elseFlag = 1
        if line.startswith("else") and elseFlag == 1:
            new_line_contents =  line.split(":",  1)[1].strip()
            elseFlag = 0
            interpret(new_line_contents, 0)
    elif line.endswith(";") != True:
        if line.startswith("//") != True:
            if line.strip():
                error(filename, number, line, "Semicolon missing")
    elif line.startswith(""):
        pass