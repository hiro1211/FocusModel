from sudachipy import dictionary, tokenizer
from math import log
from sklearn.feature_extraction.text import TfidfVectorizer


class Tfidf:

   def __init__(self):
      # sudachiの準備
      self.tokenizer_obj = dictionary.Dictionary().create()
      self.mode = tokenizer.Tokenizer.SplitMode.B

   def tfidf(self,docs, analyzer):
      # analyzerは文字列を入れると文字列のlistが返る関数
      vectorizer = TfidfVectorizer(analyzer=analyzer, min_df=1, max_df=50)
      x = vectorizer.fit_transform(docs).toarray()

      return x, vectorizer  # xはtfidf_resultとしてmainで受け取る

   def getWords(self, morphemes):
      word_list = []
      for m in morphemes:
         word_list.append(m.normalizedForm())

      # tagger = MeCab.Tagger( "-Ochasen" )
      # node = tagger.parseToNode( words.encode( "utf-8" ) )
      # while node:
      #    if node.feature.split(",")[0] == "名詞":
      #       replace_node = re.sub( re.compile( "[!-/:-@[-`{-~]" ), "", node.surface )
      #       if replace_node != "" and replace_node != " ":
      #          noun.append( replace_node )
      #    node = node.next
      return word_list

   def getTopKeywords(TF):
      list = sorted( TF.items(), key=lambda x:x[1], reverse=True )
      return list[0]

   def calcTFIDF( N,TF, DF ):
      tfidf = TF * log( N / DF )
      return tfidf


tfidf = Tfidf()
morphemes = tfidf.tokenizer_obj.tokenize("morpheme数が少なければis_skipをtrueに登録")
for m in morphemes:
   print(m.part_of_speech())
