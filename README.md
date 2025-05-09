
# Tra Cứu Phạt Nguội Tự Động

Đây là một script Python dùng để **tự động tra cứu vi phạm giao thông (phạt nguội)** theo biển kiểm soát phương tiện từ trang web chính thức của CSGT Việt Nam.

## Tính Năng

- Tự động mở trình duyệt và truy cập trang tra cứu vi phạm của CSGT.
- Nhận diện mã Captcha bằng OCR (`pytesseract` + `OpenCV`) và điền tự động.
- Thực hiện tra cứu thông tin vi phạm theo biển số và loại phương tiện.
- Lặp lại tra cứu nếu captcha sai, tối đa 10 lần/lượt.
- Tự động chạy theo lịch (ví dụ: 6h và 12h mỗi ngày).

## Yêu Cầu

- Python 3.x
- Google Chrome + [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
- Cài đặt các thư viện sau:

```bash
pip install opencv-python pytesseract numpy selenium schedule
```

- Cài đặt Tesseract OCR và chỉnh đúng đường dẫn trong code:

```python
pytesseract.pytesseract.tesseract_cmd = r'E:\Tessetact\tesseract.exe'
```

## Cấu Hình

Bạn có thể thay đổi biển số và loại phương tiện trong hàm `job()`:

```python
bien_kiem_soat = "99F-006.76"
loai_xe = "1"  # 1: ô tô, 2: xe máy, 3: xe đạp điện
```

Hoặc thay đổi lịch chạy bằng cách chỉnh:

```python
schedule.every().day.at("06:00").do(job)
schedule.every().day.at("12:00").do(job)
```

## Kỹ Thuật Nhận Diện Captcha

Script sử dụng OpenCV để làm sạch hình ảnh Captcha và `pytesseract` để nhận diện mã xác thực. Việc xử lý ảnh bao gồm:
- Chuyển sang grayscale
- Làm mờ nhẹ và nhị phân hóa ảnh
- Sử dụng cấu hình `--psm 7` để nhận diện chính xác hơn một dòng ký tự

## Demo/Kết Quả

Ví dụ kết quả đầu ra:

```
Đang chờ đến giờ chạy...
Thử lần 1
Mã captcha: x3hf9z
Tra cứu thành công:
Biển số xe 99F-006.76: Không tìm thấy vi phạm phạt nguội.
```

## Lưu Ý

- Captcha trên trang có thể thay đổi, nên OCR có thể không chính xác 100%.
- Trang web có thể thay đổi cấu trúc HTML, có thể khiến script không hoạt động nếu không cập nhật kịp thời.


