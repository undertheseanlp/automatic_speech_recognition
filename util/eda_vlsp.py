from os import listdir
from os.path import join, dirname
import pandas as pd
import numpy as np
import librosa

ROOT_FOLDER = dirname(dirname(__file__))


def stat_tokens(lines):
    token_lengths = [len(line.split()[1:]) for line in lines]
    token_lengths = pd.Series(token_lengths)
    print(token_lengths.describe(percentiles=np.linspace(0, 1, 21)))


def stat_text():
    print("\nText Data:")
    text_file = join(ROOT_FOLDER, "data", "vlsp", "text")
    lines = open(text_file, "r").read().splitlines()
    print("VLSP 2018 DATA SET")
    print("\nTotal sentences:", len(lines))
    stat_tokens(lines)


def stat_acoustic():
    print("\nAcoustic Data:")
    wav_folder = join(ROOT_FOLDER, "data", "vlsp", "wav")
    files = listdir(wav_folder)
    files = [join(wav_folder, file) for file in files]
    durations = [librosa.get_duration(filename=file) for file in files]
    durations = pd.Series(durations)
    print(f"Total: {durations.sum():.2f} seconds ({durations.sum() / 3600:.2f} hours)")
    print(durations.describe())


if __name__ == '__main__':
    stat_text()
    stat_acoustic()
