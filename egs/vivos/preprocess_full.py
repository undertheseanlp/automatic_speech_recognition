import shutil
from os import mkdir, walk,listdir,path
from os.path import dirname
from os.path import join
import os
import re
import subprocess

def create_train_waves():

    waves_folder = join(dirname(dirname(dirname(__file__))), "data", "vivos",
         "raw","train","waves")
    waves_folder_2 = join(dirname(dirname(dirname(__file__))), "data", "vivos",
         "raw","test","waves")
    waves_folder_3 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt",
                          "raw", "FPTOpenSpeechData_Set001_V0.1", "mp3")
    waves_folder_4 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt",
                          "raw", "FPTOpenSpeechData_Set002_V0.1", "mp3")
    corpus_waves_folder = join(dirname(dirname(dirname(__file__))), "data", "vivos",
         "corpus","train","wav")
    try:
        shutil.rmtree(corpus_waves_folder)
    except:
        pass
    finally:
        mkdir(corpus_waves_folder)

    list_files = os.listdir(waves_folder_3)
    list_files.sort()

    for f in list_files:
        real_file_path = join(waves_folder_3, f)
        des_file_path = path.abspath("{}/global_{}".format(corpus_waves_folder, f.replace(".mp3", ".wav").replace("_","")))
        if f[-3:] == "mp3":
            # TODO - Convert mp3 into wav with sox to mono
            subprocess.call(['ffmpeg', '-i', real_file_path, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',
                             des_file_path])
        pass

    list_files2 = os.listdir(waves_folder_4)
    list_files2.sort()

    for f in list_files2:
        real_file_path = join(waves_folder_4, f)
        des_file_path = path.abspath(
            "{}/global_{}".format(corpus_waves_folder, f.replace(".mp3", ".wav").replace("_", "")))
        if f[-3:] == "mp3":
            # TODO - Convert mp3 into wav with sox to mono
            subprocess.call(['ffmpeg', '-i', real_file_path, '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '16000',
                             des_file_path])
        pass


    for root, dirs, files in walk(waves_folder):
        for dir in dirs:
            for f in listdir(join(waves_folder, dir)):
                shutil.copy(
                    join(waves_folder, dir, f),
                    join(corpus_waves_folder, f))

    for root, dirs, files in walk(waves_folder_2):
        for dir in dirs:
            for f in listdir(join(waves_folder_2, dir)):
                shutil.copy(
                    join(waves_folder_2, dir, f),
                    join(corpus_waves_folder, f))


def create_test_waves():
    waves_folder = join(dirname(dirname(dirname(__file__))), "data", "vlsp",
         "wav")
    corpus_waves_folder = join(dirname(dirname(dirname(__file__))), "data", "vivos",
         "corpus","test")
    try:
        shutil.rmtree(corpus_waves_folder)
    except:
        pass
    finally:
        mkdir(corpus_waves_folder)

    shutil.copytree(waves_folder,join(corpus_waves_folder,"wav"))
    files = listdir(join(corpus_waves_folder,"wav"))
    for file in files:
        os.rename(join(corpus_waves_folder,"wav",file),join(corpus_waves_folder,"wav","{}_{}".format("global",file)))
    list_files = listdir(join(corpus_waves_folder,"wav"))
    list_files.sort()


def create_train_text():
    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos",
         "raw","train","prompts.txt")
    content_path2 = join(dirname(dirname(dirname(__file__))), "data", "vivos",
                        "raw", "test", "prompts.txt")
    content_path3 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt","raw",
                         "FPTOpenSpeechData_Set001_V0.1", "transcript.txt")
    content_path4 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt", "raw",
                         "FPTOpenSpeechData_Set002_V0.1", "transcript.txt")

    content = open(content_path).read()
    content = content.replace(":", "")

    content2 = open(content_path2).read()
    content2 = content2.replace(":", "")

    content3 = open(content_path3).read()
    content3 = content3.replace(".mp3|","|")
    content3 = re.sub(r'\|(\d*\.*\-*)*\n','\n', content3)

    content4 = open(content_path4).read()
    content4 = content4.replace(".mp3|", "|")
    content4 = re.sub(r'\|(\d*\.*\-*)*\n', '\n', content4)

    lines = content.splitlines()
    lines2 = content2.splitlines()

    lines3 = content3.splitlines()
    lines4 = content4.splitlines()

    output = []

    for line in lines3:
        content = "global_{}".format(line.replace("_",""))
        output.append(content)

    for line in lines4:
        content = "global_{}".format(line.replace("_",""))
        output.append(content)

    for line in lines:
        items = line.split()
        fileid = items[0]
        text = " ".join(items[1:]).lower()
        content = "{}|{}".format(fileid, text)
        output.append(content)
    for line in lines2:
        items = line.split()
        fileid = items[0]
        text = " ".join(items[1:]).lower()
        content2 = "{}|{}".format(fileid, text)
        output.append(content2)
    text = "\n".join(output)

    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos","corpus","train", "text")
    open(content_path, "w").write(text)


def create_test_text():
    content_path = join(dirname(dirname(dirname(__file__))), "data", "vlsp", "text")

    content = open(content_path).read()
    content = content.replace(":", "")
    lines = content.splitlines()
    output = []
    for line in lines:
        m = re.match(r"^(?P<fileid>.*)\t(?P<text>.*)$", line)
        if m:
            text = m.group("text")
            fileid = m.group("fileid")
            content = "{}|{}".format("global_{}".format(fileid), text)
            output.append(content)
    text = "\n".join(output)


    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "test", "text")
    open(content_path, "w").write(text)



def create_gender():
    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "raw", "train", "genders.txt")
    content = open(content_path).read()

    content_path2 = join(dirname(dirname(dirname(__file__))), "data", "vivos", "raw", "test", "genders.txt")
    content2 = open(content_path2).read()

    content = content2 + content + "global m" + "\n"

    output_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "train", "gender")
    open(output_path, "w").write(content)

    content_test = "\n".join(["global m"])

    output_test_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "test", "gender")
    open(output_test_path, "w").write(content_test)



def create_speaker():
    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "raw", "train", "prompts.txt")
    content_path2 = join(dirname(dirname(dirname(__file__))), "data", "vivos", "raw", "test", "prompts.txt")
    content_path3 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt", "raw",
                         "FPTOpenSpeechData_Set001_V0.1", "transcript.txt")
    content_path4 = join(dirname(dirname(dirname(__file__))), "data", "open_fpt", "raw",
                         "FPTOpenSpeechData_Set002_V0.1", "transcript.txt")
    lines = open(content_path).read().splitlines()
    files = [line.split()[0] for line in lines]
    tmp = []

    lines3 = open(content_path3).read().splitlines()
    lines4 = open(content_path4).read().splitlines()

    for line in lines3:
        m = re.match(r"^(?P<fileid>.*).mp3", line)
        if m:
            fileid = m.group("fileid")
            content = "global {}".format("global_{}".format(fileid.replace("_","")))
            tmp.append(content)

    for line in lines4:
        m = re.match(r"^(?P<fileid>.*).mp3", line)
        if m:
            fileid = m.group("fileid")
            content = "global {}".format("global_{}".format(fileid.replace("_","")))
            tmp.append(content)

    for file_id in files:
        speaker_id = file_id.split("_")[0]
        content = "{} {}".format(speaker_id, file_id)
        tmp.append(content)

        # Merge vivos test to train dir
    lines2 = open(content_path2).read().splitlines()
    files2 = [line.split()[0] for line in lines2]

    for file_id in files2:
        speaker_id = file_id.split("_")[0]
        content = "{} {}".format(speaker_id, file_id)
        tmp.append(content)

    tmp.sort()

    content = "\n".join(tmp)

    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "train", "speaker")
    open(content_path, "w").write(content)

    lines_test_path = join(dirname(dirname(dirname(__file__))), "data", "vlsp", "text")
    lines_test = open(lines_test_path).read().splitlines()
    test_output = []

    for line in lines_test:
        # print(line)
        m = re.match(r"^(?P<fileid>.*)\t(?P<text>.*)$", line)
        if m:
            # text = m.group("text")
            fileid = m.group("fileid")
            content = "global {}".format("global_{}".format(fileid))

            test_output.append(content)
    content_path = join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "test", "speaker")
    content = "\n".join(test_output)
    open(content_path, "w").write(content)


try:
    shutil.rmtree(join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus"))
except:
    pass
finally:
    mkdir(join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus"))
    mkdir(join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus","train"))
    mkdir(join(dirname(dirname(dirname(__file__))), "data", "vivos", "corpus", "test"))
    create_train_waves()
    create_test_waves()
    create_train_text()

    create_test_text()
    create_gender()
    create_speaker()
