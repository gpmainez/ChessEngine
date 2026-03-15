import sys
from UniFun import readSentence, readStream


def isValid(sentence):
    if not sentence: return False
    if(sentence[-1] in "?!"): return True
    return False

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue

        if isValid(sentence):
            sys.stdout.write(sentence +"\n")
#jedyne co to ze jesli nw plik bedzie zle zformatowany i amsz linie z samymi ????? np to wysweitli
#i taka juz mocna chamowa jesli jest cytat konczocy sie znakiem zapytania to nie wysweitlasz koncu cytatu
# iz  tego robi sie klopot w takim przypadku Kto tam? – zapytał.
def main():
    print_sentences(readSentence(readStream()))


if __name__ == "__main__":
    main()
