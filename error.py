def error(filename, line, text, message):
    line = line + 1
    print("File \"" + filename + "\", " + str(line))
    print(text)
    print(message)