import numpy as np
import string
import pymorphy2
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re


def preprocess(name):
    # print(name)
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    result = []

    for line in name:

        line = line.lower()
        line = line.replace('»', ' ')
        for t in line:
            if t in string.punctuation:

                line = line.replace(t, ' ')
        # line = line2.join([t for t in line if t not in string.punctuation])
        line = [t for t in line.split() if t not in stopwords.words('russian')]
        temp = []
        for word in line:
            temp.append(word)
            # temp.append(morph.parse(word)[0].normal_form)
        result += [temp]
    return result

# with open('site_1.txt', encoding="utf-8") as file:
#     name = [row.strip() for row in file]

dataset = []

for i in range(1, 101):
    print(i)
    with open('sites/site_' + str(i) + '.txt', encoding="utf-8") as file:
        name = [row.strip() for row in file]


    for item in preprocess(name):
        dataset += item

    r = re.compile("[а-яА-Я]+")
    dataset = [w for w in filter(r.match, dataset)]

dataset = list(dict.fromkeys(dataset))
with open('tokens2.txt', "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(item + '\n')
print(dataset)
print(len(dataset))


