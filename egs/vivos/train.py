from egs.vivos.extension.model import KaldiSpeechRecognition
from os.path import join, dirname
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--kaldi_folder', help='Kaldi dir path', required=True)
parser.add_argument('--corpus_folder', help='Corpus path to train',required=True)
parser.add_argument('--export_path', help='Export path will be able soon')
parser.add_argument('--nj', help='Parallel number of job', default=1)
parser.add_argument('--method', help='Parallel number of job', default="deltadelta")


args = parser.parse_args()


def train(kaldi_folder, corpus_folder, export_folder=None, nj=1, method="deltadelta"):
    export_folder = join(dirname(__file__), "model")
    params = {
        "method": method,
        "jobs": nj,
        "lm_order": 1
    }
    model = KaldiSpeechRecognition(corpus_folder, kaldi_folder, params)
    model.fit()


if __name__ == "__main__":
    train(args.kaldi_folder, args.corpus_folder, args.export_path,args.nj,args.method)