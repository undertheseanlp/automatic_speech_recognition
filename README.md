# Nhận dạng tiếng nói tiếng Việt

Dự án nghiên cứu về bài toán *Nhận dạng tiếng nói tiếng Việt*, thuộc nhóm nghiên cứu về xử lý ngôn ngữ tự nhiên tiếng Việt - [underthesea](https://github.com/undertheseanlp/). Chứa mã nguồn để xử lý dữ liệu, huấn luyện và đánh giá các mô hình. Bạn cũng có thể mở rộng bằng cách huấn luyện mô hình cho bài toán của riêng bạn.  

## Nhóm tác giả 

* Vũ Anh ([anhv.ict91@gmail.com](anhv.ict91@gmail.com))
* Lê Phi Hùng &lt;lephihungch@gmail.com&gt;

Mọi ý kiến đóng góp hoặc yêu cầu trợ giúp xin gửi vào mục [Issues](/issues) của dự án. Các thảo luận được khuyến khích **sử dụng tiếng Việt** để dễ dàng trong quá trình trao đổi. 

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


