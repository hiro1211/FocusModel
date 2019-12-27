import MeCab
import sys
import re
from collections import Counter
from gensim.models import KeyedVectors
from gensim.test.utils import datapath


nwjc_model = KeyedVectors.load_word2vec_format(
    datapath('/home/ymaki/word2vec_model/nwjc_sudachi_full_abc_w2v/nwjc.sudachi_full_abc_w2v.txt'),
    binary=False
)

# ê, ³
print(len(nwjc_model.vocab), nwjc_model.vector_size)

print(nwjc_model.most_similar('コーラ', topn=5))


print(nwjc_model.most_similar(positive=['王子', '女'], negative=['男'], topn=5))

def analyze_mecab(infile):
    # infile = "/home/ymaki/Investigation-workspace/Phycho/res/discourse/UGM007-1_2Kana.txt"
    with open(infile, encoding="utf-8") as f:
        data = f.read()

    texts = data.split('\n')
    for text in texts:
        text = text.split("(")[0][3:] if  text.startswith("○") else text.split("(")[0]
        if(len(text) < 1):
            continue

        print(text)
        parse = MeCab.Tagger().parse(text)
        print(parse)
        print("=======================")



    # parse1 = MeCab.Tagger("-Ochasen").parse(text)
    # print(parse1)
    # print("*************************")
    # lines = parse.split("\n")
    # items = (re.split('[\t,]', line) for line in lines)

    # for item in items:
    #     print("i"+str(item))