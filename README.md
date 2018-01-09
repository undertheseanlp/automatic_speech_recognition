# Vietnamese Speech Recognition


## Huấn luyện mô hình



## Môi trường

* Ubuntu 16.04

## Cài đặt

**Cài đặt Kaldi** theo hướng dẫn tại [http://kaldi-asr.org/doc/tutorial_setup.html](http://kaldi-asr.org/doc/tutorial_setup.html)

**Cài đặt language modeling toolkit srilm**

Tải [srilm](https://github.com/denizyuret/nlpcourse/blob/master/download/srilm-1.7.0.tgz) sau đó lưu trong thư mục `kaldi-trunk/tools` với tên srilm.tgz

Cài đặt dependencies

```
$ apt-get install gawk
```

Cài đặt srilm

```
$ cd kaldi-trunk/tools
$ ./install_srilm.sh
...
Installation of SRILM finished successfully
Please source the tools/env.sh in your path.sh to enable it
```