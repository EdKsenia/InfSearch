import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
import pymorphy2

count = 101
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

# def create_tokens():
#     result={}
#     for i in range(1, 101):
#         dataset = []
#         with open('site_' + str(i) + '.txt', encoding="utf-8") as file:
#             name = [row.strip() for row in file]
#         for item in preprocess(name):
#             dataset += item
#         r = re.compile("[а-яА-Я]+")
#         dataset = [w for w in filter(r.match, dataset)]
#         # task3
#         dataset = list(dict.fromkeys(dataset))
#         for token in dataset:
#             if token in result.keys():
#                 result[token].append(i)
#             else:
#                 result[token] = [i]
#     return result

# с кол-вом повторений
def create_tokens2():
    result={}
    words_count={}
    for i in range(1, count):
        dataset = []
        with open('sites/site_' + str(i) + '.txt', encoding="utf-8") as file:
            name = [row.strip() for row in file]
        for item in preprocess(name):
            dataset += item
        r = re.compile("[а-яА-Я]+")
        dataset = [w for w in filter(r.match, dataset)]
        j = str(i)
        for token in dataset:
            if token in result.keys() and j in result[token].keys():
                result[token].update({j: result[token].get(j)+1})
            elif token in result.keys() and j not in result[token].keys():
                (result[token])[j] = 1
            else:
                result[token] = {j: 1}
        words_count[i] = len(dataset)
    return result, words_count

tokens,words_count = create_tokens2()

with open('test_inverted_indexes.txt', "w", encoding="utf-8") as f:
    for key in tokens:
        f.write('{\"count\":' + str(len(tokens[key])) +
                ',\"inverted_array\":' + str(tokens[key]) +
                ',\"word\":\"' + str(key) + '\"}\n')

with open('test_words_count.txt', "w", encoding="utf-8") as f:
    for key in words_count:
        f.write('{\"page\":' + str(key) + ',\"count\":' + str(words_count[key]) + '}\n')

def create_lemms(tokens):
    lemms = {}
    lemms_stat = {}
    for token in tokens:
        morph = pymorphy2.MorphAnalyzer(lang='ru')
        norm_form = morph.parse(token)[0].normal_form
        if norm_form in lemms.keys():
            lemms[norm_form].append(token)
        else:
            lemms[norm_form] = [token]
        if norm_form in lemms_stat.keys():
            for k, v in (tokens[token]).items():
                if k in lemms_stat[norm_form].keys():
                    (lemms_stat[norm_form])[k] += v
                else:
                    (lemms_stat[norm_form])[k] = v
        else:
            lemms_stat[norm_form] = {}
            lemms_stat[norm_form].update(tokens[token])
    return lemms, lemms_stat

lemms, lemms_statictic = create_lemms(tokens)

with open('test_lemms.txt', "w", encoding="utf-8") as f:
    for key in lemms:
        f.write(key + ': ')
        for token in lemms[key]:
            f.write(token + ' ')
        f.write('\n')

with open('test_lemms_stat.txt', "w", encoding="utf-8") as f:
    for key in lemms_statictic:
        f.write('{\"count\":' + str(len(lemms_statictic[key])) +
                ',\"inverted_array\":' + str(lemms_statictic[key]) +
                ',\"word\":\"' + str(key) + '\"}\n')


