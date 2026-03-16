from uni_fun import read_stream, read_sentence

def is_valid(sentence):
    if sentence.count(",") > 1: return True #nie wystarczy imo
    return False

def get_first(sentenceStream):
    for sentence in sentenceStream:
        if is_valid(sentence): return sentence

    return ""
#liczysz chyba przecinki czyli wyliczanie blednie ci zaznaczy jakko zdanie podzredne np
#firma to ula, Ola. -> zwroci a to nie ma zdanai podrzednego chyba ze nie ogarniam
#tak samo gdy przecinek to separator liczb 10 np 67,67

def main():
    sentence = get_first(read_sentence(read_stream()))
    print(sentence)

if __name__ == "__main__":
    main()