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
