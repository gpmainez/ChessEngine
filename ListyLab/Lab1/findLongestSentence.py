from UniFun import readSentence, readStream

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
    result = find_longest_sentence(readSentence(readStream()))
    print(result)

if __name__ == "__main__":
    main()