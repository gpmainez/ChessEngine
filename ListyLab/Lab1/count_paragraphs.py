import sys
from uni_fun import read_stream


def count_par():
    count = 0
    in_paragraph = False
    bufor = ""

    for char in read_stream():
        if char == "\n":
            if bufor.strip() != "":
                if in_paragraph:
                    count += 1
                    in_paragraph = False
            else:
                in_paragraph = True

            bufor = ""
        else:
            bufor += char

    #jesli nie endline
    if bufor.strip() != "" and not in_paragraph:
        count += 1

    return count

def main():
    result = count_par()
    sys.stdout.write(str(result) + "\n")

if __name__ == "__main__":
    main()