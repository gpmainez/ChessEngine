import sys

def read():
    bufor = ""
    c = sys.stdin.read(1)
    while c:
        bufor = bufor+c
        c = sys.stdin.read(1)
    return bufor

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

def iterate_sentences(text):
    sentence = ""
    for ch in text:
        sentence += ch
        if ch in ".!?":
            yield sentence.strip()
            sentence = ""
    if sentence.strip():
        yield sentence.strip()