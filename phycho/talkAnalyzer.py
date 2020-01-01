from phycho.utterance import Utterance
from pathlib import Path
from sudachi_w2v import Sudachi_w2v
from sudachipy import tokenizer
from sudachipy import dictionary
from phycho.tfidf import Tfidf
import numpy as np
from numpy import argsort

# utter_list = list()
# patientID = "UKM031"
# patientID = "UGM007"

class talk_analyzer:

    def __init__(self):
        self.path = '/home/ymaki/word2vec_model/nwjc_sudachi_full_abc_w2v/nwjc.sudachi_full_abc_w2v.txt'
        self.sudachi = dictionary.Dictionary().create()
        self.mode = tokenizer.Tokenizer.SplitMode.B

    def read(self,file):
        data = open(file, "r", encoding="utf-8")
        patientID = file.name[:6]

        utter_list = list()
        is_patient = True
        talk_num = 0
        for line in data:
            if line.startswith("○"):
                is_patient = True if line.startswith("○患者") or line.startswith("○[男女]2") else False
                talk = line[3:].split("(")[0]
            else:
                talk = line.split("(")[0]
            utter_list.append(Utterance(patientID,is_patient,talk_num,talk))

        data.close
        return utter_list

    def extract_focus_candidate(self,text):
        morpheme_list = list()
        morphemes = self.sudachi.tokenize(text,mode=self.mode)
        for m in morphemes:
            if m.part_of_speech()[0] == "名詞":
                if m.part_of_speech()[1] == "数詞":
                    continue
                morpheme_list.append(m)
            elif m.part_of_speech()[0] == "動詞":
                if m.part_of_speech()[1] == "非自立可能":
                    continue
                morpheme_list.append(m)
            elif m.part_of_speech()[0] == "形容詞":
                morpheme_list.append(m)
            else:
                continue
            # print(m.normalized_form()+"\t"+str(m.part_of_speech()))
        return morpheme_list

    def choose_focus(self,utter):
        tfidf = Tfidf()
        talk_list = list()
        for u in utter:
            talk_list.append(u.focus_wakachi)

    def to_str(self, morphemes):
        m_str = list()
        for m in morphemes:
            m_str.append(m.normalized_form())
        return m_str

    def wakachi_split(self, wakachi_text):
        return wakachi_text.split()


def main():
    analyzer = talk_analyzer()

    # フォルダ内の対象ファイルをすべて読む
    p = Path("/data/underpin/RecordVoice")
    files = p.glob("**/UGM002*Kana.txt")
    for f in files:
        utter_list = analyzer.read(f)
        print(f.name)
        wakachi_list = list()
        for u in utter_list:
            # フォーカス候補を抽出
            morphemes = analyzer.extract_focus_candidate(u.talk)

            if(u.is_skip):
                continue

            # 　■患者
            if u.is_patient is True:
                # print(str(u.talk_num) + "\t" + u.talk)
                u.focus = analyzer.choose_focus
                if morphemes is None:
                    # TODO
                    continue

            # 　■医師
            else:
                # 　　morpheme数が少なければis_skipをtrueに登録
                if morphemes is None:
                    u.is_skip = True
                    continue
                elif len(morphemes) <= 1:
                    u.is_skip = True
                    continue

            wakachi = ""
            for m in morphemes:
                wakachi+=" "+m.normalized_form()
            wakachi = wakachi[1:]
            if u.is_patient:
                print("["+u.talk+"] /"+wakachi)
            else:
                print("\t["+u.talk+"] "+wakachi)


            wakachi_list.append(wakachi)
            #TODO ここで発話ログリストに追加していく形にすると、「現在までの発話」の中のTf-idfがとれる(ハズ)
            ## omoi rasii node yameru beki?
        print(wakachi_list)

        tfidf = Tfidf()
        tfidf_X, vectorizer = tfidf.tfidf(wakachi_list, analyzer.wakachi_split)
        print(tfidf_X.shape) # (430, 489)
        index = tfidf_X.argsort(axis=1)[:, ::-1]
        feature_names = np.array(vectorizer.get_feature_names())
        print(feature_names)
        feature_words = feature_names[index]
        # フォーカスを設定　utter.focus
        #	TF-IDFから判定

        # for fwords, utter in zip(feature_words[:,0], utter_list):
        #     if utter.is_skip :
        #         print(utter.talk+"\t focus is None")
        #         continue
        #     # 各文書ごとにtarget（ラベル）とtop nの重要語を表示
        #     print(utter.talk+ " ->focus:"+fwords)
        # # for u in utter_list:



    # cos類似度を算出



    # read()
# TODO ファイル名から患者ID抽出

if __name__ == '__main__':
    main()