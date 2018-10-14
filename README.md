# Vietnamese Automatic Speech Recognition

Dự án này chứa những thử nghiệm cho bài toán *Nhận dạng tiếng nói tiếng Việt*, là một phần của dự án [underthesea](https://github.com/undertheseanlp/underthesea). Trong dự án này có chứa code để đọc dữ liệu, huấn luyện và đánh giá các mô hình. Bạn cũng có thể mở rộng bằng cách huấn luyện mô hình cho bài toán của riêng bạn.  

## Mục lục

* [Cài đặt](#cài-đặt)
* [Huấn luyện mô hình](#huấn-luyện-mô-hình)

## Cài đặt

**Môi trường thử nghiệm**

* Ubuntu 16.04

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

## Huấn luyện mô hình

**Mô tả dữ liệu**: [Xem chi tiết](data_format.md)

## Nhóm tác giả 

* Vũ Anh <anhv.ict91@gmail.com>
* Lê Phi Hùng <lephihungch@gmail.com>
