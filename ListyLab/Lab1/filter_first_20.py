
import sys
import os
from uni_fun import read_sentence, read_stream


def print_sentences(sentenceStream):
    count = 0
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue

        if count >= 20: break
        sys.stdout.write(sentence + "\n")
        count += 1

def main():
    try:
        print_sentences(read_sentence(read_stream()))
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)


if __name__ == "__main__":
    main()
