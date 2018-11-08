# Please don't charge this default config
MODEL=/home/anhv/PycharmProjects/kaldi-trunk/egs/uts_443/exp/tri2a
KALDI=/home/anhv/PycharmProjects/kaldi-trunk
WAV=/home/anhv/PycharmProjects/undertheseanlp/automatic_speech_recognition/experiment/vivos/test/VIVOSDEV01_R003.wav

# Variables
# MODEL=
# KALDI=
# WAV=

# Prepare predict dir
cd $MODEL;
rm -rf predict
mkdir predict
cd $MODEL/predict
mkdir config; mkdir experiment; mkdir transcriptions
cd $MODEL/predict/experiment
mkdir triphones_delta

# Copy pre-trained model
cd $MODEL
cp final.mdl predict/experiment/triphones_delta/final.mdl
cp -r graph predict/experiment/triphones_delta/graph

cd $MODEL/predict/config
cat > mfcc.conf << EOL
--use-energy=true
--sample-frequency=16000
--num-mel-bins=40
--frame-length=25
--frame-shift=10
--high-freq=0
--low-freq=0
--num-ceps=13
--window-type=hamming
EOL

# Prepare util
cd $MODEL/predict/transcriptions
echo "result: $WAV" > wav.scp
echo "VIVOSDEV16 result:" > spk2utt
echo "result: VIVOSDEV16" > utt2spk


# Run predict
cd $MODEL/predict;
$KALDI/src/featbin/compute-mfcc-feats \
    --config=config/mfcc.conf \
    scp:transcriptions/wav.scp \
    ark,scp:transcriptions/feats.ark,transcriptions/feats.scp
$KALDI/src/featbin/compute-cmvn-stats --spk2utt=ark:transcriptions/spk2utt \
    scp:transcriptions/feats.scp \
    ark,scp:experiment/cmvn.ark,experiment/cmvn.scp
$KALDI/src/gmmbin/gmm-latgen-faster \
    --max-active=7000 --beam=13.0 --lattice_beam=6.0 --acoustic-scale=0.83333 --allow-partial=true \
    --word-symbol-table=experiment/triphones_delta/graph/words.txt \
    experiment/triphones_delta/final.mdl \
    experiment/triphones_delta/graph/HCLG.fst \
    'ark,s,cs:$KALDI/src/featbin/apply-cmvn \
    --utt2spk=ark:transcriptions/utt2spk \
    scp:experiment/cmvn.scp \
    scp:transcriptions/feats.scp ark:- | \
    $KALDI/src/featbin/add-deltas  ark:- ark:- |' 'ark:|gzip -c > experiment/lat.JOB.gz'

echo "Finish predict"