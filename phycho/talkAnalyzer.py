from phycho.utterance import Utterance

utter_list = list()
patientID = "UKM031"
patientID = "UGM007"


# TODO フォルダ内の対象ファイルをすべて読む
# TODO ファイル名から患者ID抽出
def read():
    data = open("..\\res\\discourse\\"+patientID+"-1_1Kana.txt", "r", encoding="utf-8")

    is_patient = True
    talk_num = 0
    for line in data:
        talk = None
        if line.startswith("○"):
            is_patient = True if line.startswith("○患者") else False
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


read()
for u in utter_list:
    print(str(u.talk_num) + "\t" + u.talk)


