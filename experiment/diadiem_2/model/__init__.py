from os.path import dirname
import os
import text

def transcript(wav_file):
    tmp_folder = dirname(__file__)
    command = "pocketsphinx_continuous -hmm {}/model_parameters/tmp.cd_cont_200 -samprate 8000 -lm {}/etc/tmp.lm -dict {}/etc/tmp.dic -infile {} -logfn yes".format(
        tmp_folder, tmp_folder, tmp_folder, wav_file)
    with os.popen(command) as c:
        output = c.read().strip()
    output = text.phone2word(output)
    return output
