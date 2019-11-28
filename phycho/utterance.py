class Utterance:
    # String   patientID;
    # boolean    isPatient; // false = 医師、true = 患者
    # int    talkNum; // 通しでの発話番号
    # String    talk;

    def __init__(self, patientID, is_patient, talk_num, talk):
        self.patientID = patientID
        self.is_patient = is_patient
        self.talk_num = talk_num
        self.talk = talk
        pass

