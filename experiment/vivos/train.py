from extension.model import KaldiSpeechRecognition
from extension.export import SphinxSpeechRecognitionExporter
from load_data import corpus_folder
from os.path import join, dirname

export_folder = join(dirname(__file__), "model")
kaldi_folder = "/home/rain/Downloads/kaldi-trunk/"

model = KaldiSpeechRecognition(corpus_folder, kaldi_folder)
# model.fit()
# SphinxSpeechRecognitionExporter.export(model, export_folder)
# wav_file = join(tmp_folder, "etc", "wav", "train", "test", "CAFPHEE003.wav")
# model.predict(wav_file)
