from os.path import dirname
import os
import text


def transcript(wav_file):
    tmp_folder = dirname(__file__)
    command = "pocketsphinx_continuous " \
              "-hmm {0}/model_parameters/tmp.cd_cont_200 " \
              "-samprate 8000 " \
              "-lm {0}/etc/tmp.lm " \
              "-dict {0}/etc/tmp.dic " \
              "-infile {1} " \
              "-logfn {0}/yes".format(tmp_folder, wav_file)
    with os.popen(command) as c:
        output = c.read().strip()
    output = text.phone2word(output)
    os.remove("{}/yes".format(tmp_folder))
    return output
