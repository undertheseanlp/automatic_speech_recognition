import json
import shutil
from extension.metrics import calculate_wer
from os.path import join, basename
import os
from underthesea.util.file_io import write
import numpy as np


class WERAnalyzeLogger:
    @staticmethod
    def log(wavs_test, texts_test, texts_pred, log_folder):
        wer = np.mean([calculate_wer(test.split(), pred.split())
                       for test, pred in zip(texts_test, texts_pred)])
        wer = np.round(wer, 4)
        result = {
            "WER": wer
        }
        content = json.dumps(result, ensure_ascii=False)
        log_file = join(log_folder, "result.json")
        write(log_file, content)
        wav_folder = join(log_folder, "wav")
        try:
            shutil.rmtree(wav_folder)
        except:
            pass
        finally:
            os.mkdir(wav_folder)
        for wav in wavs_test:
            new_path = join(wav_folder, basename(wav))
            shutil.copyfile(wav, new_path)
        wavs_test_new_path = [join("wav", basename(wav)) for wav in wavs_test]
        speech_recognition = {
            "texts_test": texts_test,
            "texts_pred": texts_pred,
            "wavs_test": wavs_test_new_path,
        }
        content = json.dumps(speech_recognition, ensure_ascii=False)
        log_file = join(log_folder, "speechrecognition.json")
        write(log_file, content)

        print("Result is written in {}".format(log_file))
        print("WER: {}%".format(wer * 100))
