from string import punctuation
from random import choice, randint
import re

def isVowel(a):
    return a in 'aeiouy'

def processSyllables(sourceSyllables):
    startsWithConsonants = [syllable for syllable in sourceSyllables if not isVowel(syllable[0])]
    numConsonants = len(startsWithConsonants)
    startsWithVowels = [syllable for syllable in sourceSyllables if isVowel(syllable[0])]
    numVowels = len(startsWithVowels)
    return {
        'consonantStart': startsWithConsonants,
        'numConsonants': numConsonants,
        'vowelStart': startsWithVowels,
        'numVowels': numVowels,
    }

def generateNames(sourceSyllables, numNames = 1, numSyllables = 2):
    consonantStart = sourceSyllables['consonantStart']
    numConsonants = sourceSyllables['numConsonants']
    vowelStart = sourceSyllables['vowelStart']
    numVowels = sourceSyllables['numVowels']
    numTotalSyllables = numConsonants + numVowels

    startWithConsonant = randint(0,1) is 0;
    previousSyllable = choice(consonantStart) if startWithConsonant else choice(vowelStart)

    names = []

    for j in range(0, numNames):
        name = []
        for i in range(0, numSyllables):
            if isVowel(previousSyllable[-1]):
                previousSyllable = choice(consonantStart)
            else:
                previousSyllable = choice(vowelStart)
            name.append(previousSyllable)
        names.append(''.join(name))

    return names

def syllySplit(word):
    word = word.strip().lower().strip(punctuation)
    splits = []
    ex = r"([^aeiouy]+y(?:[^aeiou])*(?![aeiou]))|([^aeiou]*[aeiou]+(?:[^aeiou])*)"
    for match in re.finditer(ex, word):
        s = match.start()
        e = match.end()
        splits.append(word[s:e])
    return splits
