from PyQt5.QtWidgets import QMainWindow, QLabel, QListWidgetItem
from test_form import Ui_MainWindow
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
import re
import json


class TestFormWidget(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.loadUi()
        self.btn_search.clicked.connect(self.search)

    # тут надо описать логику поиска
    def search(self):
        searching = self.search_text.text()

        dict = list(self.get_sites(self.get_binary_search(searching)))
        i = 0
        for el in dict:
            self.list_vidg.insertItem(i, el)
            i+=1

        # Имя элемента совпадает с objectName в QTDesigner

    def loadUi(self):
        # uic.loadUi('ui/test_form.ui', self)  # Загружаем дизайн
        self.setupUi(self)

    def preprocess(self, line):
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
        dataset = []
        for item in result:
            dataset += item
        r = re.compile("[а-яА-Я]+")
        dataset = [w for w in filter(r.match, dataset)]
        return dataset

    def get_words_indexes(self):
        with open('inverted_indexes.txt', encoding="utf-8") as file:
            name = [row.strip() for row in file]

        count_words = {}
        for elem in name:
            elem = elem.replace('\'', '\"')
            dictData = json.loads(elem)
            count_words[dictData["word"]] = dictData["inverted_array"]
        return count_words

    def get_sites(self, site_ids):
        with open('index.txt', encoding="utf-8") as file:
            name = [row.strip() for row in file]
        sites = {}
        for elem in name:
            dictData = json.loads(elem)
            sites[dictData["id"]] = dictData["site_url"]
        res = {}
        for id in site_ids:
            res[id] = sites[id]
        return res.values()

    def get_binary_search(self, line):
        dataset = self.preprocess(line)
        count_words = self.get_words_indexes()

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
        return res
