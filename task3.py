import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re


def preprocess(name):
    result = []

    for line in name:
        line = line.lower()
        line = line.replace('»', ' ')
        for t in line:
            if t in string.punctuation:
                line = line.replace(t, ' ')
        line = [t for t in line.split() if t not in stopwords.words('russian')]
        temp = []
        for word in line:
            temp.append(word)
        result += [temp]
    return result

# цикл по всем файлам
result={}
for i in range(1, 101):
    dataset = []
    print(i)
    with open('site_' + str(i) + '.txt', encoding="utf-8") as file:
        name = [row.strip() for row in file]
    for item in preprocess(name):
        dataset += item
    r = re.compile("[а-яА-Я]+")
    dataset = [w for w in filter(r.match, dataset)]
    dataset = list(dict.fromkeys(dataset))
    for token in dataset:
        if token in result.keys():
            result[token].append(i)
        else:
            result[token] = [i]

print(len(result))

with open('inverted_indexes.txt', "w", encoding="utf-8") as f:
    for key in result:
        f.write('{\"count\":' + str(len(result[key])) +
                ',\"inverted_array\":' + str(result[key]) +
                ',\"word\":\"' + key + '\"}\n')
