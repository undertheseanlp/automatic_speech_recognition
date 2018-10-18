import shutil
import os
import text

N = 10000


class SphinxSpeechRecognition:
    def __init__(self, corpus_folder, tmp_folder):
        print("Initial Sphinx Speech Recognition")
        self.corpus_folder = corpus_folder
        self.tmp_folder = tmp_folder
        try:
            shutil.rmtree(tmp_folder)
        except Exception as e:
            pass
        finally:
            os.mkdir(tmp_folder)
            os.system("cd {}; sphinxtrain -t tmp setup".format(tmp_folder))
        self._init_data()
        self._change_config()
        self._make_transcription()
        self._make_dictionary()
        self._make_filler()
        self._make_language_model()

    # ========================== #
    # Init Data
    # ========================== #
    def _init_data(self):
        os.system("cd {}; mkdir wav".format(self.tmp_folder))
        os.system("cd {}; mkdir wav/train".format(self.tmp_folder))
        os.system("cd {}; mkdir wav/test".format(self.tmp_folder))

        ids = open(
            "{}/train/text".format(self.corpus_folder)).read().splitlines()[:N]
        ids = [item.split("|")[0] for item in ids]
        for id in ids:
            shutil.copy2(
                "{}/train/wav/{}.wav".format(self.corpus_folder, id),
                "{}/wav/train/{}.wav".format(self.tmp_folder, id)
            )

        ids = ["train/{}".format(id) for id in ids]
        ids.append("")
        content = "\n".join(ids)
        open(os.path.join(self.tmp_folder, "etc", "tmp_train.fileids"),
             "w").write(content)

        ids = open(
            "{}/test/text".format(self.corpus_folder)).read().splitlines()
        ids = [item.split("|")[0] for item in ids]
        for id in ids:
            shutil.copy2(
                "{}/test/wav/{}.wav".format(self.corpus_folder, id),
                "{}/wav/test/{}.wav".format(self.tmp_folder, id)
            )
        ids = ["test/{}".format(id) for id in ids]
        ids.append("")
        content = "\n".join(ids)
        open(os.path.join(self.tmp_folder, "etc", "tmp_test.fileids"),
             "w").write(content)

    # ========================== #
    # Config
    # ========================== #
    def _change_config(self):
        config_file = os.path.join(self.tmp_folder, "etc", "sphinx_train.cfg")
        config = SphinxConfig(config_file)
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
    # Transcription
    # ========================== #
    def _convert_transcription(self, in_file, out_file):
        lines = open(in_file).read().splitlines()[:N]
        output = []
        for line in lines:
            fileid, word = line.split("|")
            phone = text.word2phone(word)
            content = "<s> {} </s> ({})".format(phone, fileid)
            output.append(content)
        output.append("")
        content = "\n".join(output)
        open(out_file, "w").write(content)

    def _make_transcription(self):
        self._convert_transcription(
            "{}/train/text".format(self.corpus_folder),
            "{}/etc/tmp_train.transcription".format(self.tmp_folder))
        self._convert_transcription(
            "{}/test/text".format(self.corpus_folder),
            "{}/etc/tmp_test.transcription".format(self.tmp_folder))

    # ============================== #
    # Create dictionary and phones
    # ============================== #
    def _make_dictionary(self):
        lines = open(
            "{}/train/text".format(self.corpus_folder)).read().splitlines()[:N]
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
        open("{}/etc/tmp.dic".format(self.tmp_folder), "w").write(
            "\n".join(lines))
        phone_units = sorted(set(phone_units))
        phone_units.append("SIL")
        open("{}/etc/tmp.phone".format(self.tmp_folder), "w").write(
            "\n".join(phone_units))

    def _make_filler(self):
        fillers = ["<s>", "</s>", "<sil>"]
        lines = ["{:20s}SIL".format(f) for f in fillers]
        open("{}/etc/tmp.filler".format(self.tmp_folder), "w").write(
            "\n".join(lines))

    # ========================== #
    # Language Model
    # ========================== #
    def _make_cleaned_text(self):
        in_file = "{}/train/text".format(self.corpus_folder)
        out_file = "{}/etc/text".format(self.tmp_folder)
        lines = open(in_file).read().splitlines()[:N]
        output = []
        for line in lines:
            fileid, word = line.split("|")
            phone = text.word2phone(word)
            content = "<s> {} </s>".format(phone, fileid)
            output.append(content)
        content = "\n".join(output)
        open(out_file, "w").write(content)

    def _make_language_model(self):
        self._make_cleaned_text()
        etc_folder = os.path.join(self.tmp_folder, "etc")
        chdir = "cd {}; ".format(etc_folder)
        os.system(chdir + "text2wfreq < text | wfreq2vocab > vocab")
        os.system(chdir + "text2idngram -vocab vocab -idngram idngram < text")
        os.system(
            chdir + "idngram2lm -vocab_type 0 -idngram idngram -vocab vocab -arpa tmp.lm")

    def fit(self):
        chdir = "cd {}; ".format(self.tmp_folder)
        os.system(chdir + "sphinxtrain run")

    def predict(self, wav_file):
        command = "pocketsphinx_continuous -hmm {}/model_parameters/tmp.cd_cont_200 -samprate 8000 -lm {}/etc/tmp.lm -dict {}/etc/tmp.dic -infile {} -logfn yes".format(
            self.tmp_folder, self.tmp_folder, self.tmp_folder, wav_file)
        output = os.popen(command).read().strip()
        output = text.phone2word(output)
        return output


class SphinxConfig:
    def __init__(self, config_file):
        self.file = config_file
        self.lines = open(config_file).read().splitlines()

    def save(self):
        content = "\n".join(self.lines)
        open(self.file, "w").write(content)

    def set(self, key, value):
        for i, line in enumerate(self.lines):
            if line.startswith(key):
                content = "{} = {};".format(key, value)
                self.lines[i] = content
        self.save()
