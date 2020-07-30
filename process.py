import csv
from sylly_split import syllySplit

names = []
with open('./names.txt') as file:
    names = [syllySplit(row) for row in file.readlines() if len(syllySplit(row)) > 1]
with open('./split-names.csv', 'w') as file:
    writer = csv.writer(file)
    for name in names:
        writer.writerow(row)
