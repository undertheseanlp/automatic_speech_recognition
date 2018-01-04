import configparser
from os.path import join
from languageflow.flow import Flow
import os
from util.sphinx_config import SphinxConfig
from util import text
import shutil
import subprocess


# ========================== #
# Data 
# ========================== #
def make_data():
    os.system("mkdir wav")
    os.system("cp -r ../../data/diadiem/corpus/train/wav wav/train")
    os.system("cp -r ../../data/diadiem/corpus/test/wav wav/test")

    ids = open("../../data/diadiem/corpus/train/text").read().splitlines()
    ids = [item.split("|")[0] for item in ids]
    ids = ["train/{}".format(id) for id in ids]
    ids.append("")
    content = "\n".join(ids)
    open(join("etc", "diadiem_train.fileids"), "w").write(content)

    ids = open("../../data/diadiem/corpus/test/text").read().splitlines()
    ids = [item.split("|")[0] for item in ids]
    ids = ["test/{}".format(id) for id in ids]
    ids.append("")
    content = "\n".join(ids)
    open(join("etc", "diadiem_test.fileids"), "w").write(content)


# ========================== #
# Config
# ========================== # 
def change_config():
    config = SphinxConfig()
    config.read(join("etc", "sphinx_train.cfg"))
    config.set("$CFG_BASE_DIR", "\".\"")
    config.set("$CFG_WAVFILE_SRATE", 8000.0)
    config.set("$CFG_NUM_FILT", 31)
    config.set("$CFG_LO_FILT", 200)
    config.set("$CFG_HI_FILT", 3500)
    config.set("$CFG_WAVFILE_TYPE", "'raw'")
    config.set("$CFG_LANGUAGEMODEL",
               "\"$CFG_LIST_DIR/$CFG_DB_NAME.lm\"")
    config.set("$DEC_CFG_LANGUAGEMODEL",
               "\"$CFG_BASE_DIR/etc/${CFG_DB_NAME}.lm\"")


# ========================== #
# Language Model
# ========================== #
def make_cleaned_text():
    in_file = "../../data/diadiem/corpus/train/text"
    out_file = "etc/text"
    lines = open(in_file).read().splitlines()
    output = []
    for line in lines:
        fileid, word = line.split("|")
        phone = text.word2phone(word)
        content = "<s> {} </s>".format(phone, fileid)
        output.append(content)
    content = "\n".join(output)
    open(out_file, "w").write(content)


def make_language_model():
    make_cleaned_text()
    os.chdir("etc")
    os.system("text2wfreq < text | wfreq2vocab > vocab")
    os.system("text2idngram -vocab vocab -idngram idngram < text")
    os.system(
        "idngram2lm -vocab_type 0 -idngram idngram -vocab vocab -arpa diadiem.lm")
    os.chdir("..")
    pass


# ========================== #
# Transcription
# ========================== #
def convert_transcription(in_file, out_file):
    lines = open(in_file).read().splitlines()
    output = []
    for line in lines:
        fileid, word = line.split("|")
        phone = text.word2phone(word)
        content = "<s> {} </s> ({})".format(phone, fileid)
        output.append(content)
    content = "\n".join(output)
    open(out_file, "w").write(content)


def make_transcription():
    convert_transcription("../../data/diadiem/corpus/train/text",
                          "etc/diadiem_train.transcription")
    convert_transcription("../../data/diadiem/corpus/test/text",
                          "etc/diadiem_test.transcription")


# ============================== #
# Create dictionary and phones
# ============================== #
def make_dictionary():
    lines = open("../../data/diadiem/corpus/train/text").read().splitlines()
    phones = []
    for line in lines:
        fileid, word = line.split("|")
        p = text.word2phone(word).split()
        phones += p
    phones = sorted(set(phones))
    # create .dic files
    lines = []
    phone_units = []
    for p in phones:
        units = list(p)
        phone_units += units
        units = " ".join(units)
        line = "{:20s}{}".format(p, units)
        lines.append(line)
    open("etc/diadiem.dic", "w").write("\n".join(lines))
    phone_units = sorted(set(phone_units))
    phone_units.append("SIL")
    open("etc/diadiem.phone", "w").write("\n".join(phone_units))


def make_filler():
    fillers = ["<s>", "</s>", "<sil>"]
    lines = ["{:20s}SIL".format(f) for f in fillers]
    open("etc/diadiem.filler", "w").write("\n".join(lines))


# ========================== #
# Train 
# ========================== #
def train():
    os.system("sphinxtrain run")


if __name__ == '__main__':
    # flow = Flow()
    make_data()
    change_config()
    make_transcription()
    make_dictionary()
    make_filler()
    make_language_model()
    train()
