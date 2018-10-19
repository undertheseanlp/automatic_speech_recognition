import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--wav', help='Path for input file to predict', required=True)
parser.add_argument('--kaldi_folder', help='Kaldi dir path', required=True)
parser.add_argument('--model_path', help='Model path (default: uts_{number} in kaldi-trunk/egs)')

args = parser.parse_args()


def predict(kaldi_folder, wav_file, model_path=None):
    # Model path usually is in etc at kaldi-trunk/egs/uts_{random_int}/exp
    if model_path is not None:
        model = model_path
    else:
        egs_path = "{}/egs".format(kaldi_folder)
        uts_dirs = [d for d in os.listdir(egs_path) if d.startswith("uts_")]
        if len(uts_dirs) > 0:
            model = "{}/{}".format(egs_path,uts_dirs[0])
        else:
            raise Exception("Cannot find pre-trained model in kaldi/egs folder.")

    # Prepare predict dir
    os.system("cd {}; rm -rf predict;".format(model))
    os.system("cd {}; mkdir predict;".format(model))
    os.system("cd {}/predict; mkdir config;".format(model))
    os.system("cd {}/predict; mkdir experiment;".format(model))
    os.system("cd {}/predict; mkdir transcriptions;".format(model))
    os.system("cd {}/predict/experiment; mkdir triphones_deldel;".format(model))

    # Copy pre-trained model
    os.system("cd {};cp exp/tri2a/35.mdl predict/experiment/triphones_deldel/final.mdl;".format(model))
    os.system("cd {};cp -r exp/tri2a/graph predict/experiment/triphones_deldel/graph".format(model))
    os.system("cd {}/predict/config; echo '--sample-frequency=16000 \
            \n--num-mel-bins=40 \n--frame-length=25 \n--frame-shift=10 \
            \n--high-freq=0 \n--low-freq=0 \n--num-ceps=13 \n--window-type=hamming \
            \n--use-energy=true' > mfcc.conf".format(model))
    os.system("cd {}/predict/transcriptions; echo 'test {}' > wav.scp".format(model, wav_file))
    print("done")

    # Run predict
    os.system(
        "cd {}/predict; {}/src/featbin/compute-mfcc-feats --config=config/mfcc.conf scp:transcriptions/wav.scp ark,scp:transcriptions/feats.ark,transcriptions/feats.scp" \
            .format(model, kaldi_folder))

    os.system("cd {}/predict; {}/src/featbin/add-deltas \
                      scp:transcriptions/feats.scp ark:transcriptions/delta-feats.ark" \
              .format(model, kaldi_folder))
    os.system("cd {}/predict; {}/src/gmmbin/gmm-latgen-faster \
                      --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
                      experiment/triphones_deldel/final.mdl experiment/triphones_deldel/graph/HCLG.fst \
                      ark:transcriptions/delta-feats.ark ark,t:transcriptions/lattices.ark" \
              .format(model, kaldi_folder))
    os.system("cd {}/predict; {}/src/latbin/lattice-best-path \
                      --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
                      ark:transcriptions/lattices.ark ark,t:transcriptions/one-best.tra" \
              .format(model, kaldi_folder))
    os.system("cd {}/predict; {}/utils/int2sym.pl -f 2- {}/predict/experiment/triphones_deldel/graph/words.txt transcriptions/one-best.tra \
                      > {}/predict/transcriptions/one-best-hypothesis.txt; echo $(<{}/predict/transcriptions/one-best-hypothesis.txt);" \
              .format(model, model, model, model, model))

if __name__ == "__main__":
    predict(args.kaldi_folder, args.wav, args.model_path)