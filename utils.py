from string import punctuation
from random import choice, randint
import re
import markovify

def isVowel(a):
    return a in 'aeiouy'

def startsWithConsonants(words):
    return [word for word in words if not isVowel(word[0])]
def startsWithVowels(words):
    return [word for word in words if isVowel(word[0])]

def processSyllables(sourceSyllables):
    consonantStart = startsWithConsonants(sourceSyllables)
    numConsonants = len(consonantStart)
    vowelStart = startsWithVowels(sourceSyllables)
    numVowels = len(vowelStart)
    return {
        'consonantStart': consonantStart,
        'numConsonants': numConsonants,
        'vowelStart': vowelStart,
        'numVowels': numVowels,
    }

def generateNames(data, numNames = 1, numSyllables = 2):
    sourceSyllables = data['syllables']
    consonantStart = sourceSyllables['consonantStart']
    numConsonants = sourceSyllables['numConsonants']
    vowelStart = sourceSyllables['vowelStart']
    numVowels = sourceSyllables['numVowels']
    numTotalSyllables = numConsonants + numVowels

    names = []

    for j in range(0, numNames):
        startWithConsonant = randint(0,100) < data['consonantStartOdds']
        name = [choice(consonantStart) if startWithConsonant else choice(vowelStart)]
        for i in range(1, numSyllables):
            previousSyllable = name[-1]
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
