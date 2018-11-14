#!/usr/bin/env bash
#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1


model_folder=exp/tri2a
transcript_folder=transcriptions
output_folder=output

rm -rf $output_folder
mkdir $output_folder

echo
echo "===== AUDIO -> FEATURE VECTORS ====="
echo

compute-mfcc-feats --config=conf/mfcc.conf \
    scp:$transcript_folder/wav.scp \
    ark,scp:$output_folder/feats.ark,$output_folder/feats.scp

add-deltas \
    scp:$output_folder/feats.scp \
    ark:$output_folder/delta-feats.ark


echo
echo "===== TRAINED GMM-HMM + FEATURE VECTORS -> LATTICE ====="
echo

gmm-latgen-faster \
    --word-symbol-table=$model_folder/graph/words.txt \
    $model_folder/final.mdl \
    $model_folder/graph/HCLG.fst \
    ark:$output_folder/delta-feats.ark \
    ark,t:$output_folder/lattices.ark

echo
echo "===== LATTICE -> BEST PATH THROUGH LATTICE ====="
echo

lattice-best-path \
    --word-symbol-table=$model_folder/graph/words.txt \
    ark:$output_folder/lattices.ark \
    ark,t:$output_folder/one-best.tra

echo
echo "===== BEST PATH INTEGERS -> BEST PATH WORDS ====="
echo

utils/int2sym.pl -f 2- \
    $model_folder/graph/words.txt \
    $output_folder/one-best.tra \
    > $output_folder/one-best-hypothesis.txt

cat $output_folder/one-best-hypothesis.txt
