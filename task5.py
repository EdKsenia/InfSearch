from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from pymorphy2 import MorphAnalyzer
import numpy as np
import re
from string import punctuation
from scipy import spatial
import json
import string
import nltk
from nltk.corpus import stopwords
import pymorphy2

nltk.download('stopwords')

def preprocess(line):
    line = line.lower()
    line = line.replace('»', ' ')
    for t in line:
        if t in string.punctuation:
            line = line.replace(t, ' ')
    line = [t for t in line.split() if t not in stopwords.words('russian')]
    temp = []
    for word in line:
        temp.append(word)
    return temp

def load_index():
    with open('test_lemms_stat.txt', 'r', encoding='utf-8') as file:
        lines = [row.strip() for row in file]

    lemmas_list = list()
    matrix = [[0] * 100 for _ in range(len(lines))]
    idx = 0
    for line in lines:
        line = line.replace('\'', '\"')
        dictData = json.loads(line)
        lemma = dictData["word"]

        lemmas_list.append(lemma)
        pages = dictData["inverted_array"]
        for page in pages:
            matrix[idx][int(page) - 1] = 1
        idx+=1
    return lemmas_list, np.array(matrix).transpose()

def get_vector(search_string, lemmas):
    morph = pymorphy2.MorphAnalyzer(lang='ru')
    search_tokens = preprocess(search_string)
    tokens_normal_form = [morph.parse(token)[0].normal_form for token in search_tokens]
    vector = [0] * len(lemmas)
    for token in tokens_normal_form:
        if token in lemmas:
            vector[lemmas.index(token)] = 1
    return vector

def search(search_string, lemmas, matrix):
    vector = get_vector(search_string, lemmas)

    docs = dict()
    for idx, doc in enumerate(matrix):
        if max(doc) == 1:
            docs[idx + 1] = 1 - spatial.distance.cosine(vector, doc)
        else:
            docs[idx + 1] = 0.0

    sorted_docs = sorted(docs.items(), key=lambda x: x[1], reverse=True)

    return sorted_docs

lemmas, matrix = load_index()
print(search('Звездные войны', lemmas, matrix))







