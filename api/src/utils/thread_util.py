import cv2
import pytesseract
from threading import Thread
import numpy as np
from api.src.configs import CONFIG_DECIMAL, CONFIG_STRING, CONFIG_STRING_SINGE_CHAR, CONFIG_NUMBER, KERNEL, KERNEL_MOR


class MyThread(Thread):
    """docstring for myThread"""

    def __init__(self, row_value, img_origin, label):
        super(MyThread, self).__init__()
        self.row_value = row_value
        self.img_origin = img_origin
        self.label = label
        self.obj = {}

    def run(self):
        for j, col_value in enumerate(self.row_value):
            x, y, w, h = col_value
            roi = self.img_origin[y:y + h, x:x + w]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(~gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            thresh = ~thresh
            final_image = cv2.copyMakeBorder(thresh, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            if self.label[j] == "name":
                text = pytesseract.image_to_string(final_image, lang="vie", config=CONFIG_STRING)

            elif self.label[j] == "unit":
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                med = cv2.medianBlur(gray, 3)
                text = pytesseract.image_to_string(med, lang="vie", config=CONFIG_STRING_SINGE_CHAR)

            elif self.label[j] == "price" or self.label[j] == "total_price" or self.label[j] == "money_tax" or \
                    self.label[j] == "total":
                count_white = np.sum(thresh > 0)
                count_black = np.sum(thresh == 0)
                if (count_white / count_black) < 1.5:
                    text = ""
                else:
                    # Làm đầy các text có lỗi ở trong chữ
                    boxes = pytesseract.image_to_boxes(final_image, config=CONFIG_DECIMAL)
                    text = ""
                    for b in boxes.splitlines():
                        b = b.split(' ')
                        text += b[0]
            else:
                # Làm dày text lên để tạo thành viền
                struct = cv2.getStructuringElement(cv2.MORPH_RECT, KERNEL, anchor=(-1, -1))
                dil = cv2.dilate(final_image, struct, anchor=(-1, -1), iterations=1)
                cnts = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
                # Tìm Text có
                cnts = sorted(cnts, key=lambda cnt: cv2.contourArea(cnt), reverse=True)
                for i, c in enumerate(cnts):
                    x_digit, y_digit, w_digit, h_digit = cv2.boundingRect(c)
                    # Loại các nhiễu trong ảnh. chỉ lấy lại khung của chữ
                    if h_digit > 10:
                        roi = final_image[y_digit:y_digit + h_digit, x_digit:x_digit + w_digit]
                    else:
                        roi = final_image
                        break

                # Làm đầy các text có lỗi ở trong chữ
                kernel = np.ones(KERNEL_MOR, np.uint8)
                opening = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
                roi = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
                # Đọc từng số
                boxes = pytesseract.image_to_boxes(roi, config=CONFIG_NUMBER)
                text = ""
                for b in boxes.splitlines():
                    b = b.split(' ')
                    text += b[0]

            if len(text) > 0:
                cv2.rectangle(self.img_origin, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.obj[self.label[j]] = text


def get_start(arr_thread, status):
    for i in range(len(arr_thread)):
        if status == "start":
            arr_thread[i].start()
        if status == "join":
            arr_thread[i].join()
