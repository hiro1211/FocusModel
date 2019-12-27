from phycho.utterance import Utterance
from pathlib import Path
import sudachi_w2v

# utter_list = list()
# patientID = "UKM031"
# patientID = "UGM007"

def main():
    p = Path("/data/underpin/RecordVoice")
    files = p.glob("**/UGM002*Kana.txt")

    path = '/home/ymaki/word2vec_model/nwjc_sudachi_full_abc_w2v/nwjc.sudachi_full_abc_w2v.txt'
    sudachi = sudachi_w2v(path)

    for f in files:
        # print(f)
        utter_list = read(f)
        print(f.name)
        for u in utter_list:
            if u.is_patient is True:
                print(str(u.talk_num) + "\t" + u.talk)
            else:
                print("\t" +u.talk)

    # read()


# TODO フォルダ内の対象ファイルをすべて読む
# TODO ファイル名から患者ID抽出
def read(file):
    data = open(file, "r", encoding="utf-8")
    patientID = file.name[:6]

    utter_list = list()
    is_patient = True
    talk_num = 0
    for line in data:
        talk = None
        if line.startswith("○"):
            is_patient = True if line.startswith("○患者") or line.startswith("○[男女]2") else False
            talk = line[3:].split("(")[0]
        else:
            talk = line.split("(")[0]
        if len(talk) <= 0:
            break

        utter = Utterance(patientID, is_patient, talk_num, talk)
        utter_list.append(utter)
        talk_num += 1
        # print(str(utter.talk_num)+" "+str(utter.is_patient)+"\t"+utter.talk)
        # print(utter.patientID)
    data.close
    return utter_list



if __name__ == '__main__':
    main()