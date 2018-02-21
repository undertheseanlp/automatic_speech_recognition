#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1

EXP_START=$(date +%s);

nj=1       # number of parallel jobs
lm_order=1 # language model order (n-gram quantity)

# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }

# Removing previously created data (from last run.sh execution)
rm -rf exp mfcc data/train/spk2utt data/train/cmvn.scp data/train/feats.scp data/train/split1 data/test/spk2utt data/test/cmvn.scp data/test/feats.scp data/test/split1 data/local/lang data/lang data/local/tmp data/local/dict/lexiconp.txt

echo
echo "===== PREPARING ACOUSTIC DATA ====="
echo

# Needs to be prepared by hand (or using self written scripts):
#
# spk2gender  [<speaker-id> <gender>]
# wav.scp     [<uterranceID> <full_path_to_audio_file>]
# text           [<uterranceID> <text_transcription>]
# utt2spk     [<uterranceID> <speakerID>]
# corpus.txt  [<text_transcription>]

# Making spk2utt files
utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt
utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt

echo
echo "===== FEATURES EXTRACTION ====="
echo

# Making feats.scp files
mfccdir=mfcc
# Uncomment and modify arguments in scripts below if you have any problems with data sorting
# utils/validate_data_dir.sh data/train     # script for checking prepared data - here: for data/train directory
# utils/fix_data_dir.sh data/train          # tool for data proper sorting if needed - here: for data/train directory
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/train exp/make_mfcc/train $mfccdir
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc/test $mfccdir

# Making cmvn.scp files
steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir

echo
echo "===== PREPARING LANGUAGE DATA ====="
echo

# Needs to be prepared by hand (or using self written scripts):
#
# lexicon.txt           [<word> <phone 1> <phone 2> ...]
# nonsilence_phones.txt    [<phone>]
# silence_phones.txt    [<phone>]
# optional_silence.txt  [<phone>]

# Preparing language data
utils/prepare_lang.sh data/local/dict "<UNK>" data/local/lang data/lang

echo
echo "===== LANGUAGE MODEL CREATION ====="
echo "===== MAKING lm.arpa ====="
echo

loc=`which ngram-count`;
if [ -z $loc ]; then
   if uname -a | grep 64 >/dev/null; then
           sdir=$KALDI_ROOT/tools/srilm/bin/i686-m64
   else
                   sdir=$KALDI_ROOT/tools/srilm/bin/i686
   fi
   if [ -f $sdir/ngram-count ]; then
                   echo "Using SRILM language modelling tool from $sdir"
                   export PATH=$PATH:$sdir
   else
                   echo "SRILM toolkit is probably not installed.
                           Instructions: tools/install_srilm.sh"
                   exit 1
   fi
fi

local=data/local
mkdir $local/tmp
ngram-count -order $lm_order -write-vocab $local/tmp/vocab-full.txt -wbdiscount -text $local/corpus.txt -lm $local/tmp/lm.arpa

echo
echo "===== MAKING G.fst ====="
echo

lang=data/lang
arpa2fst --disambig-symbol=#0 --read-symbol-table=$lang/words.txt $local/tmp/lm.arpa $lang/G.fst

echo
echo "===== MONO TRAINING ====="
echo

START=$(date +%s);
steps/train_mono.sh --nj $nj \
  --cmd "$train_cmd" data/train data/lang exp/mono  || exit 1
END=$(date +%s);
MONO_TRAINING_TIME=$((END - START))

echo
echo "===== MONO DECODING ====="
echo

START=$(date +%s);
utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 1 --cmd "$decode_cmd" \
  exp/mono/graph data/test exp/mono/decode
END=$(date +%s);
MONO_DECODING_TIME=$((END - START))

echo
echo "===== MONO ALIGNMENT ====="
echo

START=$(date +%s);
steps/align_si.sh --nj $nj --cmd "$train_cmd" \
  data/train data/lang exp/mono exp/mono_ali || exit 1
END=$(date +%s);
MONO_ALIGNMENT_TIME=$((END - START))

echo
echo "===== TRI1 (first triphone pass) TRAINING ====="
echo

START=$(date +%s);
steps/train_deltas.sh --cmd "$train_cmd" 2500 20000 \
  data/train data/lang exp/mono_ali exp/tri1 || exit 1
END=$(date +%s);
TRI1_TRAINING_TIME=$((END - START))

echo
echo "===== TRI1 (first triphone pass) DECODING ====="
echo

START=$(date +%s);
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 1 --cmd "$decode_cmd" \
  exp/tri1/graph data/test exp/tri1/decode
END=$(date +%s);
TRI1_DECODING_TIME=$((END - START))

echo
echo "===== TRI1 ALIGNMENT ====="
echo

START=$(date +%s);
steps/align_si.sh --nj $nj --cmd "$train_cmd" \
  data/train data/lang exp/tri1 exp/tri1_ali || exit 1;
END=$(date +%s);
TRI1_ALIGNMENT_TIME=$((END - START))

echo
echo "===== TRI2A TRAINING ====="
echo

START=$(date +%s);
steps/train_deltas.sh --cmd "$train_cmd" 2500 20000 \
  data/train data/lang exp/tri1_ali exp/tri2a || exit 1
END=$(date +%s);
TRI2A_TRAINING_TIME=$((END - START))

echo
echo "===== TRI2A DECODING ====="
echo

START=$(date +%s);
utils/mkgraph.sh data/lang exp/tri2a exp/tri2a/graph || exit 1
steps/decode.sh --config conf/decode.config --nj 1 --cmd "$decode_cmd" \
  exp/tri2a/graph data/test exp/tri2a/decode
END=$(date +%s);
TRI2A_DECODING_TIME=$((END - START))

echo
echo "===== TRI2A ALIGNMENT ====="
echo

START=$(date +%s);
steps/align_si.sh --nj $nj --cmd "$train_cmd" \
  data/train data/lang exp/tri2a exp/tri2a_ali || exit 1;
END=$(date +%s);
TRI2A_ALIGNMENT_TIME=$((END - START))

echo
echo "===== run.sh script is finished ====="
echo

EXP_END=$(date +%s);
EXP_TIME=$((EXP_END - EXP_START))

log_file='exp.log'
echo "" > $log_file
echo "===== Time Report =====" >> $log_file
echo "Mono" >> $log_file
echo $MONO_TRAINING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $MONO_DECODING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $MONO_ALIGNMENT_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file

echo "Tri1" >> $log_file
echo $TRI1_TRAINING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $TRI1_DECODING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $TRI1_ALIGNMENT_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file

echo "Tri2a" >> $log_file
echo $TRI2A_TRAINING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $TRI2A_DECODING_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file
echo $TRI2A_ALIGNMENT_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file

echo "Total time:" >> $log_file
echo $EXP_TIME | awk '{print int($1/60)":"int($1%60)}' >> $log_file

echo -e "\n" >> $log_file
echo "===== Score Report =====" >> $log_file
echo "Best WER" >> $log_file
for x in exp/*/decode*; do [ -d $x ] && [[ $x =~ "$1" ]] && grep WER $x/wer_* | utils/best_wer.sh; done >> $log_file

echo -e "\n" >> $log_file

cat $log_file
