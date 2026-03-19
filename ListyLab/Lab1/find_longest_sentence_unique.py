import os
import sys
from uni_fun import read_sentence, read_stream

def is_valid(sentence):
    in_word = False
    prev_first_char = ""

    for char in sentence:
        if char.isalpha():
            if not in_word:
                in_word = True
                if char.lower() == prev_first_char.lower():
                    return False
                prev_first_char = char
        else:
            in_word = False

    return True
            
def find_longest_unique(sentenceStream):
    longest = 0
    longest_sentence = ""

    for sentence in sentenceStream:
        current_length = len(sentence)
        if is_valid(sentence) and current_length > longest:
            longest = current_length
            longest_sentence = sentence
    return longest_sentence

def main():
    sentence = find_longest_unique(read_sentence(read_stream()))
    try:
        sys.stdout.write(sentence + "\n")
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()