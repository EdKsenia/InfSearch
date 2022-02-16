import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
import re
import json


def preprocess(line):
    result = []
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


search = input()
dataset = []
for item in preprocess(search):
    dataset += item
r = re.compile("[а-яА-Я]+")
dataset = [w for w in filter(r.match, dataset)]

print(dataset)

with open('inverted_indexes.txt', encoding="utf-8") as file:
    name = [row.strip() for row in file]
# кол-во слов в кажлом файле
count_words = {}
for elem in name:
    elem = elem.replace('\'', '\"')
    dictData = json.loads(elem)
    count_words[dictData["word"]] = dictData["inverted_array"]

mas_res = {}
for word in dataset:
    if word in count_words.keys():
        mas_res[word] = count_words[word]
    else:
        mas_res[word] = []

i = 0
res = []
for elem in mas_res:
    i += 1
    if i == 1:
        res = mas_res[elem]
    else:
        res = list(set(res) & set(mas_res[elem]))

print(res)
