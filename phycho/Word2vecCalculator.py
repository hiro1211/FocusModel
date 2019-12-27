import gensim
import time
# fÌ[h
from gensim.models import KeyedVectors
from gensim.test.utils import datapath



import datetime
now = datetime.datetime.now()
print(now.strftime("%Y/%m/%d %H:%M:%S"))
print("loading...")
nwjc_model = KeyedVectors.load_word2vec_format(
    datapath('/home/ymaki/word2vec_model/nwjc_sudachi_full_abc_w2v/nwjc.sudachi_full_abc_w2v.txt'),
    binary=False
)

# ê, ³
print(len(nwjc_model.vocab), nwjc_model.vector_size)  # 3644628 300

now = datetime.datetime.now()
print(now.strftime("%Y/%m/%d %H:%M:%S"))

print("all done.")
