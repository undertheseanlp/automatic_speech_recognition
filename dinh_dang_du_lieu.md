| Phiên bản         | v1.0.0     |
|-------------------|------------|
| Lần cập nhật cuối | 10/01/2018 |
| Người thực hiện   | Vũ Anh     |

Tài liệu mô tả đề xuất về cấu trúc chuẩn của tập dữ liệu (corpus) đối với bài toán nhận dạng tiếng nói (ASR). Được áp dụng trong các thí nghiệm của [`underthesea`](https://github.com/undertheseanlp/automatic_speech_recognition) từ phiên bản 1.2.0

Các ví dụ mẫu: [`diadiem`](https://github.com/undertheseanlp/automatic_speech_recognition/tree/sphinx_lab/data/diadiem/corpus) corpus

### Tập dữ liệu

Dữ liệu của bài toán nhận dạng tiếng nói được lưu trong một thư mục, gồm hai thư mục con `train` và `test`.

* Dữ liệu huấn luyện được lưu trong thư mục `train`
* Dữ liệu kiểm thử được lưu trong thư mục `test`

Cấu trúc thư mục

```
.
├── train
|   ├── wav
|   |   ├── train_01.wav
|   |   ├── train_02.wav
|   |   └── train_03.wav
|   ├── gender
|   ├── speaker
|   └── text
└── test
    ├── wav
    |   ├── test_01.wav
    |   ├── test_02.wav
    |   └── test_03.wav
    ├── gender
    ├── speaker
    └── text
```

Mỗi thư mục `train` và `test` gồm thư mục con `wav`, file `gender`, file `speaker` và file `text`. Trong thư mục `wav` có chứa các file âm thanh (với đuôi định dạng phổ biến là wav), chứa dữ liệu âm thanh.

File `text` chứa nội dung của từng câu nói với tên file âm thanh tương ứng

*Format*: `<audio_file_id>|<text content>`

```
train_01|text content 01
train_02|text content 02
train_03|text content 03
train_04|text content 04
```

File `speaker` chứa mô tả speaker id với câu nói tương ứng

*Format*: `<speaker_id> <audio_file_id>`

```
spk01 train_01
spk01 train_02
spk02 train_03
spk02 train_04
```

File `gender` chứa thông tin về giới tính của speaker

*Format*: `<speaker_id> <gender>`

```
spk01 f
spk02 m
```

Ký hiệu:

* `f` (female): speaker có giới tính nữ
* `m` (male): speakder có giới tính nam