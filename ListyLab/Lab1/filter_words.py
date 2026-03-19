import sys,os
from uni_fun import read_stream, read_sentence

def contains_words(sentence: str) -> bool:
    valid_words = "/i/oraz/ale/że/lub/" 
    matches = 0
    current_word = ""
    
    for char in sentence:
        if char.isalpha():
            current_word += char.lower()
        else:
            if current_word:
                if "/" + current_word + "/" in valid_words:
                    matches += 1
                    if matches >= 2:
                        return True
                current_word = ""
     #fallback           
    if current_word:
        if "/" + current_word + "/" in valid_words:
            matches += 1

    return matches >= 2

def print_sentences(sentenceStream):
    for sentence in sentenceStream:
                #informacja o akapicie
        if sentence == "\n":
            sys.stdout.write("\n") 
            continue
        
        if not sentence:
            continue
            
        if contains_words(sentence):
            sys.stdout.write(sentence + "\n")

def main():
    try:    
        print_sentences(read_sentence(read_stream()))
        sys.stdout.flush()
        os._exit(0)
    except (BrokenPipeError, OSError):
        os._exit(0)
if __name__ == "__main__":
    main()