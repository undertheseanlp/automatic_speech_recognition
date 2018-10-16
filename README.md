# Nhận dạng tiếng nói tiếng Việt

Dự án nghiên cứu về bài toán *Nhận dạng tiếng nói tiếng Việt*, thuộc nhóm các dự án nghiên cứu và phát triển xử lý ngôn ngữ tự nhiên tiếng Việt - [undertheseanlp](https://github.com/undertheseanlp/). Chứa các mã nguồn để xử lý dữ liệu, huấn luyện và đánh giá các mô hình, cũng như dễ dàng tùy chỉnh mô hình cho những dữ liệu mới.  

**Nhóm tác giả**

* Vũ Anh ([anhv.ict91@gmail.com](anhv.ict91@gmail.com))
* Lê Phi Hùng ([lephihungch@gmail.com](lephihungch@gmail.com))

**Đóng góp**

Mọi ý kiến đóng góp hoặc yêu cầu trợ giúp xin gửi vào mục [Issues](../../issues) của dự án. Các thảo luận được khuyến khích **sử dụng tiếng Việt** để dễ dàng trong quá trình trao đổi. 

Nếu bạn có kinh nghiệm trong bài toán này, muốn tham gia vào nhóm phát triển với vai trò là [Developer](https://docs.google.com/document/d/1o8is5rf1Co62YWn4xu8kIAgSh54_sHeOnnR-0HSKY68/edit#heading=h.wbhllzwe8ncq), xin hãy đọc kỹ [Hướng dẫn tham gia](https://docs.google.com/document/d/1o8is5rf1Co62YWn4xu8kIAgSh54_sHeOnnR-0HSKY68/edit#heading=h.wbhllzwe8ncq).

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


Trước khi run train.py phải set lại đường dẫn tới kaldi_folder .

Method predict nên có thêm argument model_path nếu bạn đã thực hiện train trước đó (vì nếu không nó sẽ lấy theo tmp_path của model, mà tmp_path này random cho mỗi lần khởi tạo lại model để chuẩn bị cho việc chạy training mới)

Thay đổi N_TRAIN và N_TEST trong init của KaldiSpeechRecognition để đổi giới hạn tập train/test

Output folder sẽ nằm trong kaldi_folder/egs/uts_{tmp_number} với tmp_number được thấy khi run train.py (EX: "Init Kaldi Speech Recognition in number_of_tmp folder" - Will be updated soon)
