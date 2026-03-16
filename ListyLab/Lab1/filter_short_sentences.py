import sys
from uni_fun import read_sentence, read_stream

def count_words(sentence: str) -> int:
    word_count = 0
    in_word = False
    
    for char in sentence:
        if char.isalpha():
            if not in_word:
                in_word = True
                word_count += 1
        else:
            in_word = False
            
    return word_count

def print_short(sentenceStream):
    for sentence in sentenceStream:
        #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue
        
        if count_words(sentence) <= 4:
            sys.stdout.write(sentence+"\n")

    return ""

def main():
    print_short(read_sentence(read_stream()))


if __name__ == "__main__":
    main()