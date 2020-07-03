# IMPORTS
import sys

# VARIABLE DECLARATIONS
variables = []

def interpret(line, number):
    if line.startswith("print"):
        new_line_contents = line.replace("print", "").strip()
        if "INTEGER" in line:
            final_line_contents = new_line_contents.replace("INTEGER", "").strip()
            try:
                final_int = int(final_line_contents)
                print(final_int)
            except ValueError:
                print("ERROR: VALUE IS NOT AN INTEGER")
                error = True
        elif "DECIMAL" in line:
            final_line_contents = new_line_contents.replace("DECIMAL", "").strip()
            try:
                final_float = float(final_line_contents)
                print(final_float)
            except ValueError:
                print("ERROR: VALUE IS NOT A DECIMAL")
        elif "STRING" in line:
            final_line_contents = new_line_contents.replace("STRING", "").strip()
            print(final_line_contents)
        elif "var" in line:
            final_line_contents = new_line_contents.replace("var", "").strip()
            varListLength = len(variables)
            for i in range(varListLength):
                var = variables[i]
                var2 = "".join(str(e) for e in var)
                if final_line_contents in var2:
                    print(var2.replace(final_line_contents, "").strip())
                    
    if line.startswith("var"):
        new_line_contents = line.replace("var", "").strip()
        variableName = new_line_contents.split("=", 1)[0]
        value = new_line_contents.split("=", 1)[1]
        variables.append([variableName, value])

    if line.startswith("//"):
        pass


def setup(filename):
    read_lines = filename.readlines()
    read_lines_stripped = [line.strip("\n") for line in read_lines]
    read_lines_enum = enumerate(read_lines_stripped)
    for count, item in read_lines_enum:
        interpret(item, count)
def main():
    file = open(sys.argv[1])
    setup(file)

main()