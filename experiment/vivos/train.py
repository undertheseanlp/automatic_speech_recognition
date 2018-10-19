from experiment.vivos.extension.model import KaldiSpeechRecognition
from experiment.vivos.load_data import corpus_folder
from os.path import join, dirname


export_folder = join(dirname(__file__), "model")
kaldi_folder = "/Users/rj/Downloads/kaldi-trunk"
params = {
    "method": "deltadelta",
    "jobs": 1,
    "lm_order": 1
}
model = KaldiSpeechRecognition(corpus_folder, kaldi_folder, params)
model.fit()

