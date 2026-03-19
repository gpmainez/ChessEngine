import os
import sys
from uni_fun import read_sentence, read_stream

def has_capital_word(sentence):
    word_count = 0
    in_word = False
    for char in sentence:
        if char.isalpha():
            if not in_word:
                in_word = True
                word_count +=1

                if char.isupper() and word_count > 1:
                    return True
        else:
            in_word = False

    return False

def percent_of_sentences():
    total = 0
    with_capital = 0
    for sentence in read_sentence(read_stream()):
        if sentence == "\n":
            continue

        total += 1
        if has_capital_word(sentence):
            with_capital += 1
    if total == 0:
        return -1.0
    return (with_capital / total) * 100.0

def main():
    result = percent_of_sentences()
    try:
        sys.stdout.write(f"{result:.2f}\n")
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)

if __name__ == "__main__":
    main()