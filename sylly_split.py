from string import punctuation
import re

def syllySplit(word):
    word = word.strip().lower().strip(punctuation)
    splits = []
    ex = r"([^aeiouy]+y(?:[^aeiou])*(?![aeiou]))|([^aeiou]*[aeiou]+(?:[^aeiou])*)"
    #ex = r"([^aeiouy]+y(?:[^aeiou])*(?![aeiou]))|([^aeiou]*[aeiou]+[^aeiou])"
    for match in re.finditer(ex, word):
        s = match.start()
        e = match.end()
        splits.append(word[s:e])
    return splits
