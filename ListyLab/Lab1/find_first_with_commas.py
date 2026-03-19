import os
import sys

from uni_fun import read_stream, read_sentence

def is_valid(sentence):
    if sentence.count(",") > 1: return True
    return False

def get_first(sentenceStream):
    for sentence in sentenceStream:
        if is_valid(sentence): return sentence

    return ""

def main():
    sentence = get_first(read_sentence(read_stream()))
    try:
        sys.stdout.write(sentence + "\n")
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()