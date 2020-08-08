from string import punctuation
from random import choice, randint
import re
import markovify

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

class SyllaMarkov(markovify.Text):
    def word_join(self, words):
        """
        Words are actually letters in this model.
        """
        return ''.join(words);

    def word_split(self, word):
        """
        A sentence is a name and is split into letters.
        """
        return list(word);

    def sentence_split(self, text):
        """
        Sentences are actually individual names comma seperated.
        """
        if not isinstance(text, list):
            return text.split(',');
        return text;

    def sentence_join(self, sentences):
        """
        Sentences should be joined by commas.
        """
        return ','.join(sentences);

    def make_name(self, max_syllables = 4, min_syllables = 2):
        """
        Forked from default sentence behavior to allow for syllable lengths to be
        provided instead of character counts.

        Attempts 15 tries to generate a valid name with max 70% overlap and max
        5 characters of overlap.

        If successful, returns the name. If not, returns None.

        Syllable count will be bounded by `max_syllables`(default 4) and
        `min_syllables`(default 2).
        """
        tries = 15
        mor = 0.7
        mot = 5

        for _ in range(tries):
            name = [] + self.chain.walk(None)
            syllables = syllySplit(''.join(name));
            if (max_syllables != None and len(syllables) > max_syllables) or (min_syllables != None and len(syllables) < min_syllables):
                continue # pragma: no cover # see https://github.com/nedbat/coveragepy/issues/198
            if hasattr(self, "rejoined_text"):
                if self.test_sentence_output(name, mor, mot):
                    return self.word_join(name)
            else:
                return self.word_join(name)
        return None
