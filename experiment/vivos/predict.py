import os
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--wav', help='Path for input file to predict', required=True)
parser.add_argument('--kaldi_folder', help='Kaldi dir path', required=True)
parser.add_argument('--model_path', help='Model path (default: exp/{model} in kaldi-trunk/egs/{result})', required=True)
parser.add_argument('--utils_path', help='Kaldi utils dir path, usually in super parent directory of model_path')
parser.add_argument('--method', help='Method to predict, delta/lda_mllt,sat',default="delta")

args = parser.parse_args()


def predict(kaldi_folder, wav_file, model_path,method="delta", utils_path=None):
    # Model path usually is in etc at kaldi-trunk/egs/uts_{random_int}/exp
    model = model_path

    if not os.path.exists(os.path.join(model,"final.mdl")):
        raise Exception("Cannot find final.mdl model file with given model path.")
    if not os.path.exists(os.path.join(model, "graph")):
        raise Exception("Cannot find graph with given model path.")

    if utils_path is None:
        utils_path = os.path.join(os.path.dirname(os.path.dirname(model)), "utils")

    if not os.path.exists(os.path.join(utils_path,"int2sym.pl")):
        raise Exception("Cannot find int2sym.pl file with given utils path, please make sure that you are provided correctly utils_path argument")

    # Prepare predict dir
    os.system("cd {}; rm -rf predict;".format(model))
    os.system("cd {}; mkdir predict;".format(model))
    os.system("cd {}/predict; mkdir config;".format(model))
    os.system("cd {}/predict; mkdir experiment;".format(model))
    os.system("cd {}/predict; mkdir transcriptions;".format(model))
    os.system("cd {}/predict/experiment; mkdir triphones_deldel;".format(model))

    # Copy pre-trained model
    os.system("cd {};cp final.mdl predict/experiment/triphones_deldel/final.mdl;".format(model))

    os.system("cd {};cp -r graph predict/experiment/triphones_deldel/graph".format(model))

    os.system("cd {}/predict/config; echo '--use-energy=true \n\
            --sample-frequency=16000 \n\
            --num-mel-bins=40 \n\
            --frame-length=25 \n\
            --frame-shift=10 \n\
            --high-freq=0 \n\
            --low-freq=0 \n\
            --num-ceps=13 \n\
            --window-type=hamming' > mfcc.conf".format(model))
    os.system("cd {}/predict/transcriptions; echo 'result: {}' > wav.scp".format(model, wav_file))
    os.system("cd {}/predict/transcriptions; echo 'VIVOSDEV16 result:' > spk2utt".format(model))
    os.system("cd {}/predict/transcriptions; echo 'result: VIVOSDEV16' > utt2spk".format(model))
    # os.system("cd {}/predict/transcriptions; echo 'VIVOSDEV02-R015 result' > utt2spk".format(model))

    # Run predict
    os.system(
        "cd {}/predict; {}/src/featbin/compute-mfcc-feats --config=config/mfcc.conf \
        scp:transcriptions/wav.scp ark,scp:transcriptions/feats.ark,transcriptions/feats.scp"\
            .format(model, kaldi_folder))

    os.system(
        "cd {}/predict; {}/src/featbin/compute-cmvn-stats --spk2utt=ark:transcriptions/spk2utt \
        scp:transcriptions/feats.scp ark,scp:experiment/cmvn.ark,experiment/cmvn.scp" \
            .format(model, kaldi_folder))

    # os.system(
    #     "cd {}/predict; {}/src/featbin/apply-cmvn --uut2spk=ark:transcriptions/utt2spk \
    #     scp:transcriptions/feats.scp ark,scp:experiment/cmvn.ark,experiment/cmvn.scp" \
    #         .format(model, kaldi_folder))

    #delta
    if method == "delta":
        # os.system("cd {}/predict; {}/src/featbin/add-deltas \
        #                   scp:transcriptions/feats.scp ark:transcriptions/delta-feats.ark" \
        #           .format(model, kaldi_folder))


        # os.system("cd {}/predict; {}/src/gmmbin/gmm-latgen-faster \
        # --max-active=7000 --beam=13.0 --lattice_beam=6.0 --acoustic-scale=0.83333 --allow-partial=true \
        #                   --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
        #                   experiment/triphones_deldel/final.mdl \
        #                   experiment/triphones_deldel/graph/HCLG.fst \
        #                   ark:transcriptions/delta-feats.ark \
        #                   ark,t:transcriptions/lattices.ark" \
        #           .format(model, kaldi_folder))
        os.system("cd {}/predict; {}/src/gmmbin/gmm-latgen-faster \
                --max-active=7000 --beam=13.0 --lattice_beam=6.0 --acoustic-scale=0.83333 --allow-partial=true \
                                  --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
                                  experiment/triphones_deldel/final.mdl \
                                  experiment/triphones_deldel/graph/HCLG.fst \
                                  'ark,s,cs:{}/src/featbin/apply-cmvn \
                                  --utt2spk=ark:transcriptions/utt2spk \
                                  scp:experiment/cmvn.scp \
                                  scp:transcriptions/feats.scp ark:- | \
                                  {}/src/featbin/add-deltas  ark:- ark:- |' 'ark:|gzip -c > experiment/lat.JOB.gz'"\
                  .format(model, kaldi_folder,kaldi_folder,kaldi_folder))

    elif method == "lda_mllt":
        os.system("cd {};cp final.mat predict/experiment/triphones_deldel/final.mat;".format(model))

        os.system("cd {}/predict; {}/src/featbin/splice-feats \
               scp:transcriptions/feats.scp \
               ark:transcriptions/splice-feats.ark".format(model,kaldi_folder))
        os.system("cd {}/predict; {}/src/featbin/transform-feats \
                  experiment/triphones_deldel/final.mat \
                  ark:transcriptions/splice-feats.ark \
                  ark:transcriptions/splice-transform-feats.ark".format(model,kaldi_folder))
        os.system("cd {}/predict; {}/src/gmmbin/gmm-latgen-faster \
                          --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
                          experiment/triphones_deldel/final.mdl experiment/triphones_deldel/graph/HCLG.fst \
                          ark:transcriptions/splice-transform-feats.ark ark,t:transcriptions/lattices.ark" \
                  .format(model, kaldi_folder))
    else:
        raise Exception("The given method {} is not supported yet".format(method))

    os.system("cd {}/predict; {}/src/latbin/lattice-best-path \
                      --word-symbol-table=experiment/triphones_deldel/graph/words.txt \
                      ark:transcriptions/lattices.ark \
                      ark,t:transcriptions/one-best.tra" \
              .format(model, kaldi_folder))
    os.system("cd {}/predict; {}/int2sym.pl -f 2- {}/predict/experiment/triphones_deldel/graph/words.txt transcriptions/one-best.tra \
                      > {}/predict/transcriptions/one-best-hypothesis.txt; echo $(<{}/predict/transcriptions/one-best-hypothesis.txt);" \
              .format(model, utils_path, model, model, model))

    result = open("{}/predict/transcriptions/one-best-hypothesis.txt".format(model)).read()
    #Result will stored in model_path/predict/transcriptions/one-best-hypothesis.txt under format test {predict_result}
    result = result[8:]
    print(result)
    return result

if __name__ == "__main__":
    predict(args.kaldi_folder, args.wav, args.model_path, args.method, args.utils_path)