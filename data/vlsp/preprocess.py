import shutil
from os import mkdir, walk
from os import listdir
from os.path import join
import re


def create_corpus_dataset():
    corpus_train_waves_folder = "corpus/train/wav"
    corpus_test_waves_folder = "corpus/test/wav"
    org_text = "text"
    #
    lines = open(org_text).read().splitlines()
    train_output = []
    test_output = []
    speaker_test = []
    speaker_train = []
    gender_test = []
    gender_train = []
    i = 0
    total_records = len(lines)
    for line in lines:
        # print(line)
        m = re.match(r"^(?P<fileid>.*)\t(?P<text>.*)$", line)
        if m:
            text = m.group("text")
            fileid = m.group("fileid")
            content = "{}|{}".format(fileid, text)
            if i < total_records * 90 / 100:
                train_output.append(content)
                shutil.copyfile("wav/{}.wav".format(fileid),"{}/{}.wav".format(corpus_train_waves_folder,fileid))
                speaker_train.append("{} {}".format("global",fileid, fileid))

            else:
                test_output.append(content)
                shutil.copyfile("wav/{}.wav".format(fileid), "{}/{}.wav".format(corpus_test_waves_folder, fileid))
                speaker_test.append("{} {}".format("global", fileid,fileid))

            i += 1
        else:
            raise Exception("Content not match.")
    train_text = "\n".join(train_output)
    test_text = "\n".join(test_output)
    speaker_train_text = "\n".join(speaker_train)
    speaker_test_text = "\n".join(speaker_test)
    gender_train_text = "\n".join(["global m"])
    gender_test_text = "\n".join(["global m"])
    open("corpus/train/text", "w").write(train_text)
    open("corpus/test/text", "w").write(test_text)
    open("corpus/train/gender", "w").write(gender_train_text)
    open("corpus/test/gender", "w").write(gender_test_text)
    open("corpus/train/speaker", "w").write(speaker_train_text)
    open("corpus/test/speaker", "w").write(speaker_test_text)


try:
    shutil.rmtree("corpus")
except:
    pass
finally:
    mkdir("corpus")
    mkdir("corpus/train")
    mkdir("corpus/test")
    mkdir("corpus/train/wav")
    mkdir("corpus/test/wav")

    create_corpus_dataset()
