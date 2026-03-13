import sys

def pararg():
    count = 0
    emptyLine = True
    for line in sys.stdin:
        line = line.strip()
        if line == "":
            count += 1
        else:
            if emptyLine:
                count += 1
            emptyLine = False
    print(count)

if __name__ == "__main__":
    pararg()