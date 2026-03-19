import os
import sys

from uni_fun import read_sentence, read_stream

def find_longest_sentence(sentence_stream):
    longest = 0
    longest_sentence = ""
    
    for sentence in sentence_stream:
        current_length = len(sentence)
        if current_length > longest:
            longest = current_length
            longest_sentence = sentence

    return longest_sentence

def main():
    result = find_longest_sentence(read_sentence(read_stream()))
    try:
        sys.stdout.write(result + "\n")
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()