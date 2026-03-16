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


def read_stream():
    while True:
        try:
            char = sys.stdin.read(1)
            if not char: break
            yield char

        except IOError: break

def read_sentence(char_stream):
    buffer = ""
    prev_char = ""
    
    for char in char_stream:
        #koniec akapitu
        if char == "\n" and prev_char == "\n":
            if buffer.strip() != "":
                yield clean(buffer)
            yield "\n"
            buffer = ""
            prev_char = char
            continue

        #yieldujemy dopiero jak dotrzemy do nowego zdania, a nie jak znajdziemy znak interpunkcujny, dzieki temu zabezpieczamy sie na ... iraz ?!
        if prev_char in ".!?" and char not in ".!?":
            if buffer.strip() != "":
                yield clean(buffer)
            buffer = ""
            
        buffer += char
        prev_char = char
        
    #fallback
    if buffer.strip() != "":
        yield clean(buffer)