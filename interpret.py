import sys
from ast import literal_eval
from error import *
sys.setrecursionlimit(5000)

# VARIABLE DECLARATIONS
variables = []
arrays = []
functions = []
filename = ""

elseFlag = 0

def setFilename(fileParam):
    global filename
    filename = fileParam

def Math(input):
    return eval(input)

def import_file(fileToImport):
    file = open(fileToImport)
    read_lines = file.readlines()
    read_lines_stripped = [line.strip("\n") for line in read_lines]
    read_lines_enum = enumerate(read_lines_stripped)
    for count, item in read_lines_enum:
        if item.startswith("print") == False: 
            interpret(item, count)

def interpret(line, number):
    global elseFlag
    if line.endswith(";") or line.endswith("{") or line.endswith("}"):
        if line.startswith("//"):
            pass
        for i in range(0, len(variables)):
            if line.startswith(variables[i][0]):
                    value = line.replace(variables[i][0], "").replace("=",  "").replace(";", "").strip()
                    if value.startswith("Math"):
                        value = value.replace("Math(", "").replace(")", "")
                        value = Math(value)
                        variables[i][1] = str(value)
                    elif value.startswith("inc"):
                        value = value.replace("inc(", "").replace(")", "").strip()
                        for i in range(0, len(variables)):
                            if value in variables[i][0]:
                                currentValue = variables[i][1]
                                currentValue = int(currentValue) + 1
                                variables[i][1] = str(currentValue)
                    else:
                        variables[i][1] = value
        for i in range(0, len(functions)):
            if line.startswith(functions[i][0]):
                if(functions[i][2]):
                    for j in range(0, len(functions[i][2])):
                        argumentValues = line.split("(", 1)[1].split(")", 1)[0].replace("\"", "").split(",")
                        variableName = functions[i][2][j]
                        variables.append([variableName, argumentValues[j]])  
                interpret(functions[i][1], 0)
        if line.startswith("import"):
            fileToImport = line.replace("import", "").replace("\"", "").replace(";", "").strip()
            import_file(fileToImport)
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
                        x = str(variables[i][1]).strip()
                        print(x)
                    else:
                        error(filename, number, line, "Variable \"" + final_line_contents + "\" does not exist")
        if line.startswith("function"):
            new_line_contents = line.replace("function", "").strip()
            functionName = new_line_contents.split("(", 1)[0]
            code =  new_line_contents.split(":", 1)[1].strip()
            arguments = new_line_contents.split("(", 1)[1].split(")", 1)[0].split(",")
            functions.append([functionName, code, arguments])
        if line.startswith("var"):
            new_line_contents = line.replace("var", "").strip()
            variableName = new_line_contents.split("=", 1)[0]
            value = new_line_contents.split("=", 1)[1]
            if value.replace(";", "").strip() == "True" or value.replace(";", "").strip() == "False":
                variables.append([variableName, value.replace(";", "").strip()])
            elif value.strip() == "input();":
                userInput = input()
                variables.append([variableName, userInput])
            elif value.split("(", 1)[0].strip():
                mathInput = value.replace("Math(", "").replace(")", "").replace(";", "").strip()
                output = Math(mathInput)
                variables.append([variableName, str(output)])
            else:
                if value.strip().startswith("["):
                    value = value[:-1].strip()
                    value = literal_eval(value)
                    value.insert(0, variableName)
                    arrays.append(value)
                if value.strip().startswith("\""):
                    value = value[:-1]
                    value = value.replace("\"", "")
                    variables.append([variableName, value])
                #else:
                    #print(error(filename, number, line, "Incorrect variable declaration"))
        if line.startswith("if"):
            new_line_contents = line.replace("if", "")
            if "==" in new_line_contents:
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
            elif ">=" in new_line_contents:
                variableName =  new_line_contents.split(">=", 1)[0].strip()
                new_line_contents = new_line_contents.replace(variableName, "").strip()
                new_line_contents = new_line_contents.replace(">=", "").strip()
                value = new_line_contents.split(":", 1)[0]
                varListLength = len(variables)
                for i in range(varListLength):
                    var = variables[i]
                    var2 = "".join(str(e) for e in var)
                    if variableName in var2:
                        var2 = var2.replace(variableName, "").split()
                        if int(var2[0]) >= int(value):
                            new_line_contents = line.split(":", 1)[1].strip()
                            interpret(new_line_contents, 0)
                        else:
                            elseFlag = 1
            elif "<=" in new_line_contents:
                variableName =  new_line_contents.split("<=", 1)[0].strip()
                new_line_contents = new_line_contents.replace(variableName, "").strip()
                new_line_contents = new_line_contents.replace("<=", "").strip()
                value = new_line_contents.split(":", 1)[0]
                varListLength = len(variables)
                for i in range(varListLength):
                    var = variables[i]
                    var2 = "".join(str(e) for e in var)
                    if variableName in var2:
                        var2 = var2.replace(variableName, "").split()
                        if int(var2[0]) <= int(value):
                            new_line_contents = line.split(":", 1)[1].strip()
                            interpret(new_line_contents, 0)
                        else:
                            elseFlag = 1
            elif ">" in new_line_contents:
                variableName =  new_line_contents.split(">", 1)[0].strip()
                new_line_contents = new_line_contents.replace(variableName, "").strip()
                new_line_contents = new_line_contents.replace(">", "").strip()
                value = new_line_contents.split(":", 1)[0]
                varListLength = len(variables)
                for i in range(varListLength):
                    var = variables[i]
                    var2 = "".join(str(e) for e in var)
                    if variableName in var2:
                        var2 = var2.replace(variableName, "").split()
                        if int(var2[0]) > int(value):
                            new_line_contents = line.split(":", 1)[1].strip()
                            interpret(new_line_contents, 0)
                        else:
                            elseFlag = 1
            elif "<" in new_line_contents:
                variableName =  new_line_contents.split("<", 1)[0].strip()
                new_line_contents = new_line_contents.replace(variableName, "").strip()
                new_line_contents = new_line_contents.replace("<", "").strip()
                value = new_line_contents.split(":", 1)[0]
                varListLength = len(variables)
                for i in range(varListLength):
                    var = variables[i]
                    var2 = "".join(str(e) for e in var)
                    if variableName in var2:
                        var2 = var2.replace(variableName, "").split()
                        if int(var2[0]) < int(value):
                            new_line_contents = line.split(":", 1)[1].strip()
                            interpret(new_line_contents, 0)
                        else:
                            elseFlag = 1
            elif "!=" in new_line_contents:
                            variableName =  new_line_contents.split("!=", 1)[0].strip()
                            new_line_contents = new_line_contents.replace(variableName, "").strip()
                            new_line_contents = new_line_contents.replace("!=", "").strip()
                            value = new_line_contents.split(":", 1)[0]
                            varListLength = len(variables)
                            for i in range(varListLength):
                                var = variables[i]
                                var2 = "".join(str(e) for e in var)
                                if variableName in var2:
                                    var2 = var2.replace(variableName, "").split()
                                    if int(var2[0]) != int(value):
                                        new_line_contents = line.split(":", 1)[1].strip()
                                        interpret(new_line_contents, 0)
                                    else:
                                        elseFlag = 1
        if line.startswith("else") and elseFlag == 1:
            new_line_contents =  line.split(":",  1)[1].strip()
            elseFlag = 0
            interpret(new_line_contents, 0)
        if line.startswith("for"):
            new_line_contents = line.replace("for", "")
            variableName = new_line_contents.split("in", 1)[0].strip()
            range1 = new_line_contents.split("range", 1)[1].split(",", 1)[0].strip()
            range2 = new_line_contents.split(",", 1)[1].split(":", 1)[0].strip()
            code = new_line_contents.split(":", 1)[1].strip()
            for i in range(int(range1), int(range2)):
                if len(variables) == 0:
                    variables.append([variableName, i])
                else:
                    for j in range(0, len(variables)):
                        if variableName in variables[j]:
                            del variables[j]
                            variables.append([variableName, i])
                interpret(code, 0)
            
    elif line.endswith(";") != True:
        if line.startswith("//") != True:
            if line.strip():
                error(filename, number, line, "Semicolon missing")
    elif line.startswith(""):
        pass