import shutil
from os import mkdir, walk
from os import listdir
from os.path import join


def create_train_waves():
    waves_folder = "raw/train/waves"
    corpus_waves_folder = "corpus/train/wav"
    try:
        shutil.rmtree(corpus_waves_folder)
    except:
        pass
    finally:
        mkdir(corpus_waves_folder)
    for root, dirs, files in walk(waves_folder):
        for dir in dirs:
            for f in listdir(join(waves_folder, dir)):
                shutil.copy(
                    join(waves_folder, dir, f),
                    join(corpus_waves_folder, f))


def create_test_waves():
    waves_folder = "raw/test/waves"
    corpus_waves_folder = "corpus/test/wav"
    try:
        shutil.rmtree(corpus_waves_folder)
    except:
        pass
    finally:
        mkdir(corpus_waves_folder)
    for root, dirs, files in walk(waves_folder):
        for dir in dirs:
            for f in listdir(join(waves_folder, dir)):
                shutil.copy(
                    join(waves_folder, dir, f),
                    join(corpus_waves_folder, f))


def create_train_text():
    content = open("raw/train/prompts.txt").read()
    content = content.replace(":", "")
    lines = content.splitlines()
    output = []
    for line in lines:
        items = line.split()
        fileid = items[0]
        text = " ".join(items[1:]).lower()
        content = "{}|{}".format(fileid, text)
        output.append(content)
    text = "\n".join(output)
    open("corpus/train/text", "w").write(text)


def create_test_text():
    content = open("raw/test/prompts.txt").read()
    content = content.replace(":", "")
    lines = content.splitlines()
    output = []
    for line in lines:
        items = line.split()
        fileid = items[0]
        text = " ".join(items[1:]).lower()
        content = "{}|{}".format(fileid, text)
        output.append(content)
    text = "\n".join(output)
    open("corpus/test/text", "w").write(text)


def create_gender():
    content = open("raw/train/genders.txt").read()
    open("corpus/train/gender", "w").write(content)
    content = open("raw/test/genders.txt").read()
    open("corpus/test/gender", "w").write(content)


def create_speaker():
    lines = open("raw/train/prompts.txt").read().splitlines()
    files = [line.split()[0] for line in lines]
    tmp = []
    for file_id in files:
        speaker_id = file_id.split("_")[0]
        content = "{} {}".format(speaker_id, file_id)
        tmp.append(content)
    content = "\n".join(tmp)
    open("corpus/train/speaker", "w").write(content)

    lines = open("raw/test/prompts.txt").read().splitlines()
    files = [line.split()[0] for line in lines]
    tmp = []
    for file_id in files:
        speaker_id = file_id.split("_")[0]
        content = "{} {}".format(speaker_id, file_id)
        tmp.append(content)
    content = "\n".join(tmp)
    open("corpus/test/speaker", "w").write(content)


try:
    shutil.rmtree("corpus")
except:
    pass
finally:
    mkdir("corpus")
    mkdir("corpus/train")
    mkdir("corpus/test")
    create_train_waves()
    create_test_waves()
    create_train_text()
    create_test_text()
    create_gender()
    create_speaker()
