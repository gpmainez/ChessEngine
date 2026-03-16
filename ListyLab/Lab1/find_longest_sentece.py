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
#nie rozpoznajesz ... lub tytuły np "inz. Ciapa." i program liczy inz i ciapa jako osobne zdania
#nie rozpoznajesz tez zdan rozdzielonych tabulatorem (bardziej jesli plik bylby rozjechany np zdanie takie

# No i co dalej? jedzie pociąg z daleka na nikogo nie czeka
# konduktorze
#
# laskawy.

#inie widzi laskawy
#jak sa 2 najduzsze to czy wypisywaoc oba? na rzie wypisujesz pierwsze

def main():
    result = find_longest_sentence(read_sentence(read_stream()))
    print(result)

if __name__ == "__main__":
    main()