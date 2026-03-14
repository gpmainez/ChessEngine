from UniFun import readSentence, readStream
def isValid(sentence):
    inWord = False
    prevFirstChar = ""

    for char in sentence:
        if char.isalpha():
            if not inWord:
                inWord = True
                if char.lower() == prevFirstChar.lower(): return False
                prevFirstChar = char
        else: inWord = False

    return True
            
def findLongestUnique(sentenceStream):
    longest = 0
    longestSentence = ""
    for sentence in sentenceStream:
        currentLength = len(sentence)
        if isValid(sentence) and currentLength > longest:
            longest = currentLength
            longestSentence = sentence
    return longestSentence

def main():
    sentence = findLongestUnique(readSentence(readStream()))
    print(sentence)

if __name__ == "__main__":
    main()