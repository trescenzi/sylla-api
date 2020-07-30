import csv
import sys
from random import randint

def isVowel(a):
    return a in 'aeiouy'

def getRandomPiece(pieces, numNames):
    return pieces[randint(0, numNames - 1)]

pieces = []
with open('./split-names.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        for piece in row:
            pieces.append(piece)
startsWithConsonants = [piece for piece in pieces if not isVowel(piece[0])]
numConsonants = len(startsWithConsonants)
startsWithVowels = [piece for piece in pieces if isVowel(piece[0])]
numVowels = len(startsWithVowels)

syllableLen = int(sys.argv[1])
numToGenerate = int(sys.argv[2])
numNames = len(pieces)
names = []

for j in range(0, numToGenerate):
    previousPiece = getRandomPiece(pieces, numNames)
    name = []
    for i in range(0, syllableLen):
        lastCharOfPrevious = previousPiece[len(previousPiece) - 1]
        if isVowel(lastCharOfPrevious):
            previousPiece = getRandomPiece(startsWithConsonants, numConsonants)
        else:
            previousPiece = getRandomPiece(startsWithVowels, numVowels)
        name.append(previousPiece)
    print(name)
    print(''.join(name))
    names.append(''.join(name))

with open('./out', 'w') as file:
    file.write('\n'.join(names))
