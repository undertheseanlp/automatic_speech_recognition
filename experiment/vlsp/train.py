from experiment.vlsp.extension.model import KaldiSpeechRecognition
from experiment.vlsp.load_data import corpus_folder
from os.path import join, dirname
import os


export_folder = join(dirname(__file__), "model")
kaldi_folder = "/Users/rj/Downloads/kaldi-trunk"
params = {
    "method": "deltadelta",
    "jobs": 1,
    "lm_order": 1
}
model = KaldiSpeechRecognition(corpus_folder, kaldi_folder, params)
model.fit()
# SphinxSpeechRecognitionExporter.export(model, export_folder)
wav_file = os.path.abspath("test/VIVOSDEV01_R003.wav")
model.predict(wav_file)
