# Nhận dạng tiếng nói tiếng Việt

![](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)
![](https://img.shields.io/badge/opensource-vietnamese-blue.svg)
![](https://img.shields.io/badge/build-passing-green.svg)

Dự án nghiên cứu về bài toán *Nhận dạng tiếng nói tiếng Việt*, được phát triển bởi nhóm nghiên cứu xử lý ngôn ngữ tự nhiên tiếng Việt - [undertheseanlp](https://github.com/undertheseanlp/). Chứa mã nguồn các thử nghiệm cho việc xử lý dữ liệu, huấn luyện và đánh giá mô hình, cũng như cho phép dễ dàng tùy chỉnh mô hình đối với những tập dữ liệu mới.

**Nhóm tác giả**

* Vũ Anh ([anhv.ict91@gmail.com](anhv.ict91@gmail.com))
* Lê Phi Hùng ([lephihungch@gmail.com](lephihungch@gmail.com))

**Tham gia đóng góp**

Mọi ý kiến đóng góp hoặc yêu cầu trợ giúp xin gửi vào mục [Issues](../../issues) của dự án. Các thảo luận được khuyến khích **sử dụng tiếng Việt** để dễ dàng trong quá trình trao đổi. 

Nếu bạn có kinh nghiệm trong bài toán này, muốn tham gia vào nhóm phát triển với vai trò là [Developer](https://github.com/undertheseanlp/underthesea/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-%C4%91%C3%B3ng-g%C3%B3p#developercontributor), xin hãy đọc kỹ [Hướng dẫn tham gia đóng góp](https://github.com/undertheseanlp/underthesea/wiki/H%C6%B0%E1%BB%9Bng-d%E1%BA%ABn-%C4%91%C3%B3ng-g%C3%B3p#developercontributor).

## Mục lục

* [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
* [Thiết lập môi trường](#thiết-lập-môi-trường)
* [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
  * [Sử dụng mô hình đã huấn luyện](#sử-dụng-mô-hình-đã-huấn-luyện)
  * [Huấn luyện mô hình](#huấn-luyện-mô-hình)
* [Kết quả thử nghiệm](#kết-quả-thử-nghiệm)
* [Trích dẫn](#trích-dẫn)
* [Bản quyền](#bản-quyền)

## Yêu cầu hệ thống 

* `Hệ điều hành: Ubuntu 16.04`
* `Python 3.6+`
* `conda 4+`


## Thiết lập môi trường

**Cài đặt Kaldi**

Để cài đặt Kaldi, thực hiện theo các bước tại [hướng dẫn](http://kaldi-asr.org/doc/tutorial_setup.html)

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

**Cài đặt srilm**

```
$ cd kaldi-trunk/tools
$ wget -O srilm.tgz https://raw.githubusercontent.com/denizyuret/nlpcourse/master/download/srilm-1.7.0.tgz
$ ./install_srilm.sh
...
Installation of SRILM finished successfully
Please source the tools/env.sh in your path.sh to enable it
```

## Hướng dẫn sử dụng

### Huấn luyện mô hình

**Mô tả dữ liệu**: [Xem chi tiết](data_format.md)


Trước khi run train.py phải set lại đường dẫn tới kaldi_folder .

Method predict nên có thêm argument model_path nếu bạn đã thực hiện train trước đó (vì nếu không nó sẽ lấy theo tmp_path của model, mà tmp_path này random cho mỗi lần khởi tạo lại model để chuẩn bị cho việc chạy training mới)

Thay đổi N_TRAIN và N_TEST trong init của KaldiSpeechRecognition để đổi giới hạn tập train/test

Output folder sẽ nằm trong kaldi_folder/egs/uts_{tmp_number} với tmp_number được thấy khi run train.py (EX: "Init Kaldi Speech Recognition in number_of_tmp folder" - Will be updated soon)

## Kết quả thử nghiệm 

Kết quả thử nghiệm trên tập test VLSP 2018

<table>
 <tr>
   <th>Mô hình</td>
   <th>WER</td>
 </tr>
 <tr>
    <td>TDB</td>
    <td>TDB</td>
 </tr>
</table>

## Bản quyền

Mã nguồn của dự án được phân phối theo giấy phép [GPL-3.0](LICENSE.txt).

