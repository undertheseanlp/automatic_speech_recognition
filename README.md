# Vietnamese Automatic Speech Recognition



## Huấn luyện mô hình


## Môi trường đã thử nghiệm

* Ubuntu 16.04

## Cài đặt

**Cài đặt Kaldi** theo hướng dẫn tại [http://kaldi-asr.org/doc/tutorial_setup.html](http://kaldi-asr.org/doc/tutorial_setup.html)

```
$ git clone https://github.com/kaldi-asr/kaldi.git kaldi-trunk --origin golden

$ cd kaldi-trunk/tools/; make;

$ extras/install_openblas.sh

$ cd ../src; ./configure  --openblas-root=../tools/OpenBLAS/install; make
```

**Cài đặt language modeling toolkit srilm**

Cài đặt dependencies

```
$ apt-get install gawk
```

Cài đặt srilm

```
$ cd kaldi-trunk/tools
$ wget -O srilm.tgz https://raw.githubusercontent.com/denizyuret/nlpcourse/master/download/srilm-1.7.0.tgz
$ ./install_srilm.sh
...
Installation of SRILM finished successfully
Please source the tools/env.sh in your path.sh to enable it
```

# Mô tả dữ liệu

[Xem chi tiết](đin_dang_du_lieu.md)