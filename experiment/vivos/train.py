from extension.model import SphinxSpeechRecognition
from extension.export import SphinxSpeechRecognitionExporter
from load_data import corpus_folder
from os.path import join, dirname

tmp_folder = join(dirname(__file__), "tmp")
export_folder = join(dirname(__file__), "model")

model = SphinxSpeechRecognition(corpus_folder, tmp_folder)
model.fit()
SphinxSpeechRecognitionExporter.export(model, export_folder)
# wav_file = join(tmp_folder, "etc", "wav", "train", "test", "CAFPHEE003.wav")
# model.predict(wav_file)
