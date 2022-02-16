import string
import pymorphy2
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import json
import math

def preprocess(name):
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

count = 101
with open('test_words_count.txt', encoding="utf-8") as file:
    name = [row.strip() for row in file]
# кол-во слов в кажлом файле
count_words = {}
for elem in name:
    elem = elem.replace('\'', '\"')
    dictData = json.loads(elem)
    count_words[dictData["page"]] = dictData["count"]

with open('test_inverted_indexes.txt', encoding="utf-8") as file:
    name2 = [row.strip() for row in file]
# термины/токены
tokens = {}
for elem in name2:
    elem = elem.replace('\'', '\"')
    dictData = json.loads(elem)
    tokens[dictData["word"]] = [dictData["count"], dictData["inverted_array"]]

with open('test_lemms_stat.txt', encoding="utf-8") as file:
    name3 = [row.strip() for row in file]

# леммы
lemms = {}
for elem in name3:
    elem = elem.replace('\'', '\"')
    dictData = json.loads(elem)
    lemms[dictData["word"]] = [dictData["count"], dictData["inverted_array"]]


result = []
result_lemms = []
for i in range(1, count):
    result.append({})
    result_lemms.append({})

for token in tokens:
    # в скольких текстах встречается
    words_doc = tokens[token][0]
    # в каких документах и сколько раз
    page_count = tokens[token][1]
    for page in page_count:
        result[int(page)-1].update({token:[page_count[page]/count_words[int(page)],
                                  math.log(100/words_doc)]})

for lemm in lemms:
    # в скольких текстах встречается
    lemm_doc = lemms[lemm][0]
    # в каких документах и сколько раз
    lemm_page_count = lemms[lemm][1]
    for page in lemm_page_count:
        result_lemms[int(page)-1].update({lemm:[lemm_page_count[page]/count_words[int(page)],
                                  math.log(100/lemm_doc)]})

for i in range(1,count):
    with open('tf_idf/test_tokens_tf_idf_' + str(i) + '.txt', "w", encoding="utf-8") as f:
        for key in result[i-1]:
            f.write(key + ' ' + str(result[i-1][key][1]) + ' ' + str(result[i-1][key][0]) + '\n')
    with open('tf_idf/test_lemms_tf_idf_' + str(i) + '.txt', "w", encoding="utf-8") as f:
        for key in result_lemms[i-1]:
            f.write(key + ' ' + str(result_lemms[i-1][key][1]) + ' ' + str(result_lemms[i-1][key][0]) + '\n')

