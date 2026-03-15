import sys

def clean(line):
    result = ""
    prev_space = False
    for ch in line:
        if ch in " \t\n\r":
            if not prev_space:
                result += " "
            prev_space = True
        else:
            result += ch
            prev_space = False
    return result.strip()


def readStream():
    while True:
        try:
            char = sys.stdin.read(1)
            if not char: break
            yield char

        except IOError: break

def readSentence(char_stream):

    buffer = ""
    prev_char = ""
    for char in char_stream:
        buffer += char

        if char in ".!?": #kon zdania
            yield clean(buffer)
            buffer = ""
        elif char == "\n" and prev_char == "\n":
            if buffer.strip() != "":
                yield clean(buffer)
            yield "\n"
            buffer = ""
            
        prev_char = char
       #zabezpieczenie ostanie zdanie
    if buffer.strip() != "":
        yield clean(buffer)     
