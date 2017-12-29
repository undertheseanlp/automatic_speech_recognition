# Vietnamese Speech Recognition

## Môi trường

* Ubuntu 16.04

## Cài đặt

Cài đặt sphinx 4 theo hướng dẫn tại [Installing CMU-Sphinx on Ubuntu](http://jrmeyer.github.io/asr/2016/01/08/Installing-CMU-Sphinx-on-Ubuntu.html)

* Cài đặt sphinxbase
* Cài đặt sphinxtrain
* Cài đặt pocketsphinx
* Cài đặt cmuclmtk

## Huấn luyện mô hình HMM

```
cd huanluyen_diadiem
sphinxtrain train
```

## Predict

Lấy ra kết quả với input đầu vào là một file wav trong tập test

```
cd huanluyen_diadiem
pocketsphinx_continuous -hmm model_parameters/huanluyen_diadiem.cd_cont_200 -dict etc/huanluyen_diadiem.dic -samprate 8000 -lm etc/huanluyen_diadiem.lm.DMP -infile wav/test/CAFPHEE004.wav
```

Chỉ predict ra kết quả text

```
pocketsphinx_continuous -hmm model_parameters/huanluyen_diadiem.cd_cont_200 -samprate 8000 -lm etc/huanluyen_diadiem.lm.DMP -dict etc/huanluyen_diadiem.dic -infile Voice_004.wav -logfn yes
DDUSNG KHASCH SAJN
```

Predict ra kết quả text với thời gian tương ứng

```
pocketsphinx_continuous -hmm model_parameters/huanluyen_diadiem.cd_cont_200 -samprate 8000 -lm etc/huanluyen_diadiem.lm.DMP -dict etc/huanluyen_diadiem.dic -infile Voice_004.wav -logfn yes -time yes
DDUSNG KHASCH SAJN
<s> 0.250 0.270 0.999900
<sil> 0.280 0.400 0.654719
DDUSNG 0.410 0.900 0.758106
<s> 0.910 1.010 0.938655
KHASCH 1.020 1.510 1.000000
SAJN 1.520 2.210 1.000000
</s> 2.220 2.290 1.000000
```

