import numpy as np
import pickle
import re
import csv
import os
from sudachipy import tokenizer
from sudachipy import dictionary

class Sudachi_w2v:
    def __init__(self, path, sudachiDataPath="sudachiData.pickle"):
        f = open(path, 'r')
        self.file = f
        self.reader = csv.reader(f, delimiter=' ')
        #ÅÉÜLPêXgâAhXXgðì¬·éi©ÈèÔ©©éj
        #2ñÚÈ~Ípickle»µ½àÌðÇÝÞ
        if os.path.exists(sudachiDataPath):
            with open(sudachiDataPath, 'rb') as f:
                dataset = pickle.load(f)
            self.offset_list = dataset["offset_list"]
            self.emb_size = dataset["emb_size"]
            self.word2index = dataset["word2index"]
            self.ave_vec = dataset["ave_vec"]
        else:
            txt = f.readline()
            #ªU\»Ì³
            self.emb_size = int(txt.split()[1])
            #¢mêª½ê½ÏxNgðÔ·
            self.ave_vec = np.zeros(self.emb_size, np.float)
            #AhXXg
            self.offset_list = []
            word_list = []
            count = 0
            maxCount = int(txt.split()[0])
            while True:
                count+=1
                self.offset_list.append(f.tell())
                if count % 100000 == 0:print(count,"/",maxCount)
                line = f.readline()
                if line == '':break
                line_list = line.split()
                word_list.append(line_list[0])
                self.ave_vec += np.array(line_list[-300:]).astype(np.float)
            self.offset_list.pop()
            self.ave_vec = self.ave_vec/count
            self.word2index = {v:k for k,v in enumerate(word_list)}

            dataset = {}
            dataset["offset_list"] = self.offset_list
            dataset["emb_size"] = self.emb_size
            dataset["word2index"] = self.word2index
            dataset["ave_vec"] = self.ave_vec
            with open(sudachiDataPath, 'wb') as f:
                pickle.dump(dataset, f)

        self.num_rows = len(self.offset_list)
        #sudachiÌõ
        self.tokenizer_obj = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.C

    #PêðxNg»
    def word2vec(self, word):
        try:
            idx = self.word2index[word]
            result = self.read_row(idx)
            vec = np.array(result[-300:])
            return vec
        except:#PêXgÉÈ¢ê
            print(word, ": out of wordlist")

    #¶Íðª©¿«µ½ãC»ê¼êÌxNgðmatÅÜÆßÄÔ·
    def sentence2mat(self, sentence):
        words = sentence.replace("@"," ").replace("\n"," ")
        words = re.sub(r"\s+", " ", words)
        input_seq = [m.surface().lower() for m in self.tokenizer_obj.tokenize(words, self.mode)]
        input_seq = [s for s in input_seq if s != ' ']

        mat = np.zeros((len(input_seq), self.emb_size))
        input_sentence = []
        for i, word in enumerate(input_seq):
            try:
                idx = self.word2index[word]
                result = self.read_row(idx)
                input_sentence.append(result[0])
                mat[i] = np.array(result[-300:])
            except:#PêXgÉÈ¢ê½ÏxNgðÔ·
                input_sentence.append("<UNK>")
                mat[i] = self.ave_vec
        return input_sentence, mat

    def __del__(self):
        self.file.close()

    def read_row(self, idx):
        self.file.seek(self.offset_list[idx])
        return next(self.reader)

path = '/home/ymaki/word2vec_model/nwjc_sudachi_full_abc_w2v/nwjc.sudachi_full_abc_w2v.txt'
sudachi = Sudachi_w2v(path)

vec = sudachi.word2vec("天気")
print(vec)
#['0.07975651' '0.08931299' '-0.06070593' '0.46959993' '0.19651023' ~

input_sentence, mat = sudachi.sentence2mat("今日の天気はハレです。")
print(input_sentence, mat)