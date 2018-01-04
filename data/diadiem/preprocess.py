import shutil
from os import mkdir
import re
from text import phone2word


def create_train_text():
    lines = open(
        "raw/huanluyen_diadiem_train.transcription").read().splitlines()
    output = []
    for line in lines:
        m = re.match(r"^<s> (?P<text>.*) </s> \((?P<fileid>.*)\)$", line)
        if m:
            text = phone2word(m.group("text").lower())
            fileid = m.group("fileid")
            content = "{}|{}".format(fileid, text)
            output.append(content)
            pass
        else:
            raise Exception("Content not match.")
    text = "\n".join(output)
    open("corpus/train/text", "w").write(text)


def create_test_text():
    lines = open(
        "raw/huanluyen_diadiem_test.transcription").read().splitlines()
    output = []
    for line in lines:
        m = re.match(r"^(?P<text>.*) \((?P<fileid>.*)\)$", line)
        if m:
            text = phone2word(m.group("text").lower())
            fileid = m.group("fileid")
            content = "{}|{}".format(fileid, text)
            output.append(content)
            pass
        else:
            raise Exception("Text not match.")
    text = "\n".join(output)
    open("corpus/test/text", "w").write(text)


try:
    shutil.rmtree("corpus")
except:
    pass
finally:
    mkdir("corpus")
    mkdir("corpus/train")
    mkdir("corpus/test")
    shutil.copytree("raw/wav/train", "corpus/train/wav")
    shutil.copytree("raw/wav/test", "corpus/test/wav")
    create_train_text()
    create_test_text()
