import time
import schedule
import cv2
import numpy as np
import pytesseract
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

pytesseract.pytesseract.tesseract_cmd = r'E:\Tessetact\tesseract.exe'

def lay_ma_captcha(image_path):
    # Đọc ảnh ở dạng grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Làm mịn và tăng độ tương phản
    blur = cv2.GaussianBlur(image, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Cấu hình OCR: PSM 7 = đọc 1 dòng duy nhất, whitelist giới hạn ký tự
    config = '--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789'

    # Nhận diện
    text = pytesseract.image_to_string(thresh, config=config)

    # Làm sạch: bỏ khoảng trắng, xuống dòng
    text = re.sub(r'\s+', '', text.strip().lower())

    # Kiểm tra độ dài và định dạng
    if re.fullmatch(r'[a-z0-9]{6}', text):
        return text
    else:
        print(f"Captcha sai định dạng: {text}")
        return text


def tra_cuu_vi_pham(bien_kiem_soat, loai_xe):
    """Tra cứu vi phạm."""
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")
        print(driver.title)

        for attempt in range(10):
            print(f"Thử lần {attempt + 1}")

            # Nhập biển số và loại xe
            element_bks = driver.find_element(By.NAME, 'BienKiemSoat')
            element_bks.clear()
            element_bks.send_keys(bien_kiem_soat)

            element_loai_xe = Select(driver.find_element(By.NAME, 'LoaiXe'))
            element_loai_xe.select_by_value(loai_xe)

            # Chụp lại ảnh captcha mới
            captcha_element = driver.find_element(By.ID, 'imgCaptcha')
            captcha_path = "captcha.png"
            captcha_element.screenshot(captcha_path)

            # Đọc mã captcha
            captcha_text = lay_ma_captcha(captcha_path)
            print(f"Mã captcha: {captcha_text}")

            # Nhập captcha
            element_captcha = driver.find_element(By.NAME, 'txt_captcha')
            element_captcha.clear()
            element_captcha.send_keys(captcha_text)

            # Nhấn nút tra cứu
            driver.find_element(By.CLASS_NAME, 'btnTraCuu').click()
            time.sleep(3)

            # Kiểm tra nội dung thông báo lỗi
            try:
                error_element = driver.find_element(By.CLASS_NAME, 'xe_texterror')
                error_text = error_element.text.strip()
                if "Mã xác nhận sai" in error_text:
                    print("Mã xác nhận sai, refresh để có mã đẹp hơn.")
                    driver.refresh()
                    time.sleep(2)

                else:
                    print("Tra cứu thành công:")
                    vi_pham_element = driver.find_element(By.XPATH, '//*[@id="bodyPrint123"]/div')
                    vi_pham_text = vi_pham_element.text.strip()
                    if "Không tìm thấy kết quả !" in vi_pham_text:
                        print(f"Biển số xe {bien_kiem_soat}: Không tìm thấy vi phạm phạt nguội.")                        
                    else:
                        print(f"Biển số xe {bien_kiem_soat} có vi phạm")
                    break
            except Exception as e:
                print(f"Lỗi khi tra cứu: {e}")
        else:
            print("Đã thử quá 5 lần, không thể tra cứu thành công.")

    except Exception as e:
        print(f"Lỗi khi tra cứu: {e}")
    finally:
        driver.quit()

def job():
    bien_kiem_soat = "99F-006.76"
    loai_xe = "1" #1: ô tô, 2: xe máy, 3: xe đạp điện
    
    tra_cuu_vi_pham(bien_kiem_soat, loai_xe)
# Lên lịch chạy
schedule.every().day.at("06:00").do(job)  # 6h sáng
schedule.every().day.at("12:00").do(job)  # 12h trưa

print("Đang chờ đến giờ chạy...")
while True:
    schedule.run_pending()
    time.sleep(10)