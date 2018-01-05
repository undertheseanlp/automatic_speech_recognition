from model import transcript
from os.path import join, dirname
from extension.analyze import WERAnalyzeLogger

corpus_folder = join(dirname(dirname(dirname(__file__))), "data", "diadiem",
                     "corpus")


def load_test():
    lines = open(join(corpus_folder, "test", "text")).read().splitlines()
    lines = [line.split("|") for line in lines]
    wavs = [line[0] for line in lines]
    wavs = ["{}/test/wav/{}.wav".format(corpus_folder, wav) for wav in wavs]
    texts = [line[1] for line in lines]
    return wavs, texts


wavs_test, texts_test = load_test()
# texts_pred = [""] * len(texts_test)
texts_pred = [transcript(wav_file) for wav_file in wavs_test]

log_folder = join(dirname(__file__), "analyze")

WERAnalyzeLogger.log(wavs_test, texts_test, texts_pred, log_folder=log_folder)
