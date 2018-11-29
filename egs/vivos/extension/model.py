import shutil
import os
from egs.vivos.extension.text import PhoneConverter1 as PhoneConverter
import numpy as np
from itertools import groupby

from os.path import dirname

N_TRAIN = 100
N_TEST = 10


class KaldiSpeechRecognition:
    def __init__(self,
                 corpus_folder,
                 kaldi_folder,
                 params={}):
        """ Wrapper for Kaldi Speech Recognition

        Parameters
        ----------
        params: dict
            collection of parameters for training phrase
            - jobs: number of parallel jobs
            - method: {deltadelta, lda_mllt, sat}
        """

        self.corpus_folder = corpus_folder
        self.kaldi_folder = kaldi_folder
        self.method = "deltadelta" if "method" not in params else params["method"]
        self.params = params
        id = np.random.randint(1000)
        self.id = "uts_{}".format(id)
        self.tmp_folder = "{}/egs/{}".format(self.kaldi_folder, self.id)

        train_list = os.listdir("{}/{}/wav".format(self.corpus_folder, "train"))
        test_list = os.listdir("{}/{}/wav".format(self.corpus_folder, "test"))
        self.N_TRAIN = len(train_list)
        self.N_TEST = len(test_list)


        print("Init Kaldi Speech Recognition in {} folder".format(self.id))
        self._init_env()
        self._config()
        self._audio_data()
        self._transcription()
        self._language_model()
        self._scripts()

    # ========================== #
    # Init Data
    # ========================== #
    def _init_env(self):
        os.system("cd {0}/egs; rm -rf uts*".format(self.kaldi_folder))
        os.system("cd {0}/egs; rm -f {1} | mkdir {1}".format(self.kaldi_folder,
                                                             self.id))
        os.system("cd {}; mkdir -p local".format(self.tmp_folder))
        os.system("cd {}; mkdir -p audio/train".format(self.tmp_folder))
        os.system("cd {}; mkdir -p audio/test".format(self.tmp_folder))
        os.system("cd {}; mkdir -p data/train".format(self.tmp_folder))
        os.system("cd {}; mkdir -p data/test".format(self.tmp_folder))
        os.system("cd {}; mkdir -p data/local".format(self.tmp_folder))
        os.system("cd {}; mkdir -p data/local/dict".format(self.tmp_folder))

    # ========================== #
    # Corpus Information
    # ========================== #
    def _get_speakers_utterances(self, speaker_file):
        # Get speakers and utterances
        items = open(speaker_file).read().splitlines()
        items = [item.split(" ") for item in items]
        s_u = {k: [i[1] for i in g] for k, g in
               groupby(items, key=lambda x: x[0])}
        u_s = {}
        for speaker in s_u:
            for utterance in s_u[speaker]:
                u_s[utterance] = speaker
        return s_u, u_s

    # ========================== #
    # Audio
    # ========================== #
    def _audio_data(self):
        self._copy_sound_files("train")
        self._copy_sound_files("test")
        self._create_description_files("train")
        self._create_description_files("test")

    def _copy_sound_files(self, type="train"):
        speaker_file = "{}/{}/speaker".format(self.corpus_folder, type)
        s_u, u_s = self._get_speakers_utterances(speaker_file)

        lines = open("{}/{}/text".format(self.corpus_folder, type)).read(). \
            splitlines()
        if type == "train":

            lines = lines[:self.N_TRAIN]
        else:

            lines = lines[:self.N_TEST]

        utterances = [line.split("|")[0] for line in lines]
        speakers_files = {}
        for utterance in utterances:
            speaker = u_s[utterance]
            if speaker not in speakers_files:
                speakers_files[speaker] = []
            speakers_files[speaker].append(utterance)
        for speaker in speakers_files:
            os.system(
                "cd {}; mkdir -p audio/{}/{}".format(self.tmp_folder, type,
                                                     speaker))
            for file in speakers_files[speaker]:
                infile = "{}/{}/wav/{}.wav".format(self.corpus_folder, type,
                                                   file)
                utterance = file.split("_")[1]
                outfile = "{}/audio/{}/{}/{}.wav".format(self.tmp_folder, type,
                                                         speaker, utterance)
                os.system("cp {} {}".format(infile, outfile))

    def _create_description_files(self, type):
        speaker_file = "{}/{}/speaker".format(self.corpus_folder, type)
        s_u, u_s = self._get_speakers_utterances(speaker_file)
        lines = open("{}/{}/text".format(self.corpus_folder, type)).read(). \
            splitlines()
        if type == "train":

            lines = lines[:self.N_TRAIN]
        else:

            lines = lines[:self.N_TEST]
        utterances = [line.split("|")[0] for line in lines]
        speakers = [u_s[u] for u in utterances]
        speakers = list(set(speakers))

        # spk2gender
        infile = "{0}/{1}/gender".format(self.corpus_folder, type)
        lines = open(infile).read()
        lines = lines.splitlines()
        lines = list(filter(lambda x: x.split()[0] in speakers, lines))
        content = "\n".join(lines) + "\n"
        outfile = "{}/data/{}/spk2gender".format(self.tmp_folder, type)
        open(outfile, "w").write(content)

        # spk2utt
        output = []
        speakers_files = {}
        for utterance in utterances:
            speaker = u_s[utterance]
            if speaker not in speakers_files:
                speakers_files[speaker] = []
            speakers_files[speaker].append(utterance)
        for speaker in speakers_files:
            u = speakers_files[speaker]
            u = [item.split("_")[1] for item in u]
            line = "{} {}".format(speaker, " ".join(u))
            output.append(line)
        content = "\n".join(output) + "\n"
        outfile = "{}/data/{}/spk2utt".format(self.tmp_folder, type)
        open(outfile, "w").write(content)

        # utt2spk
        output = []
        for utterance in utterances:
            speaker_id = u_s[utterance]
            utterance_id = utterance.split("_")[1]
            line = "{1}-{0} {1}".format(utterance_id, speaker_id)
            output.append(line)
        output = sorted(output, key=lambda x: x.split()[1] + x.split()[0])
        content = "\n".join(output) + "\n"
        outfile = "{}/data/{}/utt2spk".format(self.tmp_folder, type)
        open(outfile, "w").write(content)

        # wav.scp
        output = []
        for u in utterances:
            speaker_id, utterance_id = u.split("_")
            line = "{0}-{1} ./audio/{2}/{0}/{1}.wav".format(
                speaker_id, utterance_id, type)
            output.append(line)
        output = sorted(output, key=lambda x: x.split()[0])
        content = "\n".join(output) + "\n"
        outfile = "{}/data/{}/wav.scp".format(self.tmp_folder, type)
        open(outfile, "w").write(content)

    # ========================== #
    # Config
    # ========================== #
    def _config(self):
        os.system("cd {}; mkdir -p conf".format(self.tmp_folder))

        # decode.conf
        configs = [
            "first_beam=10.0",
            "beam=13.0",
            "lattice_beam=6.0"
        ]
        content = "\n".join(configs)
        outfile = "{}/conf/decode.config".format(self.tmp_folder)
        open(outfile, "w").write(content)

        # mfcc.conf
        configs = [
            "--use-energy=false  # only non-default option.",
            "--sample-frequency=16000"
        ]
        content = "\n".join(configs)
        outfile = "{}/conf/mfcc.conf".format(self.tmp_folder)
        open(outfile, "w").write(content)

    # ========================== #
    # Transcription
    # ========================== #
    def _convert_transcription(self, in_file, out_file, N):
        lines = open(in_file).read().splitlines()[:N]
        output = []
        for line in lines:
            fileid, word = line.split("|")
            speaker_id, utterance_id = fileid.split("_")
            content = "{}-{} {}".format(speaker_id, utterance_id, word)
            output.append(content)
        output = sorted(output, key=lambda x: x.split()[0])
        output.append("")
        content = "\n".join(output)
        open(out_file, "w").write(content)

    def _corpus_txt(self):
        train_text_file = "{}/train/text".format(self.corpus_folder)
        train_text = open(train_text_file).read().splitlines()[:self.N_TRAIN]
        test_text_file = "{}/test/text".format(self.corpus_folder)
        test_text = open(test_text_file).read().splitlines()[:self.N_TEST]
        text = train_text + test_text
        text = [item.split("|")[1] for item in text]
        content = "\n".join(text)
        open("{}/data/local/corpus.txt".format(self.tmp_folder), "w").write(
            content)

    def _transcription(self):
        self._convert_transcription(
            "{}/train/text".format(self.corpus_folder),
            "{}/data/train/text".format(self.tmp_folder), self.N_TRAIN)
        self._convert_transcription(
            "{}/test/text".format(self.corpus_folder),
            "{}/data/test/text".format(self.tmp_folder), self.N_TEST)


        self._corpus_txt()

    # ============================== #
    # Create dictionary and phones
    # ============================== #
    def _scripts(self):
        pwd = dirname(__file__)

        # cmd.sh
        shutil.copy2(
            "{}/cmd.sh".format(pwd),
            "{}/cmd.sh".format(self.tmp_folder)
        )

        # path.sh
        shutil.copy2(
            "{}/path.sh".format(pwd),
            "{}/path.sh".format(self.tmp_folder)
        )

        # run.sh
        content = open("{}/run_{}.sh".format(pwd, self.method)).read()
        script_file = "{}/run.sh".format(self.tmp_folder)
        with open(script_file, "w") as f:
            if "jobs" in self.params:
                jobs = "nj={}".format(self.params["jobs"])
                content = content.replace("nj=1", jobs)
            if "lm_order" in self.params:
                config = "lm_order={}".format(self.params["lm_order"])
                content = content.replace("lm_order=1", config)
            f.write(content)
        os.system("chmod u+x {}".format(script_file))

        # local/score.sh
        shutil.copy2(
            "{}/../voxforge/s5/local/score.sh".format(self.tmp_folder),
            "{}/local/score.sh".format(self.tmp_folder)
        )

        # utils and steps
        shutil.copytree(
            "{}/../voxforge/s5/utils".format(self.tmp_folder),
            "{}/utils".format(self.tmp_folder)
        )

        shutil.copytree(
            "{}/../voxforge/s5/steps".format(self.tmp_folder),
            "{}/steps".format(self.tmp_folder)
        )

        # transcript.sh
        # transcript_file = "{}/transcript.sh".format(self.tmp_folder)
        # shutil.copy2(
        #     "{}/transcript_{}.sh".format(pwd, self.method),
        #     transcript_file
        # )
        # os.system("chmod u+x {}".format(transcript_file))
        #
        # shutil.copytree(
        #     "{}/transcriptions".format(pwd),
        #     "{}/transcriptions".format(self.tmp_folder)
        # )

    # ============================== #
    # Create dictionary and phones
    # ============================== #
    def _make_dictionary(self):
        lines = open(
            "{}/train/text".format(self.corpus_folder)).read().splitlines()[
                :self.N_TRAIN]
        phones = []
        for line in lines:
            fileid, word = line.split("|")
            p = PhoneConverter.word2phone(word).split()
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
        lines = open(in_file).read().splitlines()[:self.N_TRAIN]
        output = []
        for line in lines:
            fileid, word = line.split("|")
            phone = PhoneConverter.word2phone(word)
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

    def _lexicon(self):
        corpus_file = "{}/data/local/corpus.txt".format(self.tmp_folder)
        texts = open(corpus_file).read()
        words = sorted(set(texts.split()))
        phones = [list(PhoneConverter.word2phone(item)) for item in words]

        nonsilence_phones = sorted(
            set([item for sublist in phones for item in sublist]))
        outfile = "{}/data/local/dict/nonsilence_phones.txt".format(
            self.tmp_folder)
        content = "\n".join(nonsilence_phones) + "\n"
        open(outfile, "w").write(content)

        silence_phones = ["sil", "spn"]
        outfile = "{}/data/local/dict/silence_phones.txt".format(
            self.tmp_folder)
        content = "\n".join(silence_phones) + "\n"
        open(outfile, "w").write(content)

        optional_silence = ["sil"]
        outfile = "{}/data/local/dict/optional_silence.txt".format(
            self.tmp_folder)
        content = "\n".join(optional_silence) + "\n"
        open(outfile, "w").write(content)

        lexicon = (["{} {}".format(word, " ".join(phone)) for word, phone in
                    zip(words, phones)])
        lexicon = ["!SIL sil", "<UNK> spn"] + lexicon
        content = "\n".join(lexicon) + "\n"
        outfile = "{}/data/local/dict/lexicon.txt".format(self.tmp_folder)
        open(outfile, "w").write(content)

    def _language_model(self):
        self._lexicon()

    def fit(self):
        chdir = "cd {}; ".format(self.tmp_folder)
        os.system(chdir + "./run.sh")
        # os.system(chdir + "sphinxtrain run")

        def export(self,output_dir):
            #TODO: - move output from kaldi into defined output_dir
            pass



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


if __name__ == "__main__":
    pass
