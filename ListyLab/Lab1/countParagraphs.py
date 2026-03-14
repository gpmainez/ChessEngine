import sys
from UniFun import readStream

def countPar():
    count = 0
    paragraph_active = False
    bufor = ""

    for char in readStream():
        if char == "\n":
            if bufor.strip() == "":
                if paragraph_active:
                    count += 1
                    paragraph_active = False
            else:
                paragraph_active = True
            bufor = ""
        else:
            bufor += char

    #fallback
    if paragraph_active or bufor.strip() != "":
        count += 1
        
    return count

def main():
    result = countPar()
    sys.stdout.write(str(result) + "\n")

if __name__ == "__main__":
    main()