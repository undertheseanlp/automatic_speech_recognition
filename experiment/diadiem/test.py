import os
from util import text


def listen(file):
    command = "pocketsphinx_continuous -hmm model_parameters/diadiem.cd_cont_200 -samprate 8000 -lm etc/diadiem.lm -dict etc/diadiem.dic -infile {} -logfn yes".format(
        file)
    output = os.popen(command).read().strip()
    output = text.phone2word(output)
    return output


wav_files = ["wav/test/" + f for f in os.listdir("wav/test")]
wav_files = sorted(wav_files)
# wav_files = ["wav/test/KHASCHSAJN007.wav"]
for file in wav_files:
    output = listen(file)
    print("{} -> {}".format(file, output))
