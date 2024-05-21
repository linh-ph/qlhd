import cv2
import pytesseract
from threading import Thread
import numpy as np
from api.src.configs import *
import re
from pytesseract import Output
from api.src.configs import CONFIG_PATTERN_STRING_NAME_PRODUCT
import time


def post_processing_ocr_name_product(pattern, d_json):
    # print(d_json)
    json_text = []
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) != -1:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return " ".join(json_text)


def post_processing_ocr_unit_product(pattern, d_json):
    # print(d_json)
    json_text = []
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) != -1:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return " ".join(json_text)


def post_processing_ocr_price_product(pattern, d_json):
    # print(d_json)
    json_text = []
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) != -1:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return " ".join(json_text)


class MyThread(Thread):
    """docstring for myThread"""

    def __init__(self, row_value, img_origin, image_color, label):
        super(MyThread, self).__init__()
        self.row_value = row_value
        self.img_origin = img_origin
        self.image_color = image_color
        self.label = label
        self.obj = {}

    def run(self):
        for j, col_value in enumerate(self.row_value):
            x, y, w, h = col_value
            roi = self.img_origin[y:y + h, x:x + w]
            gray = roi
            thresh = cv2.threshold(~gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            thresh = ~thresh
            final_image = cv2.copyMakeBorder(thresh, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))

            if self.label[j] == "name":
                d_json = pytesseract.image_to_data(final_image, lang="vie", config=CONFIG_STRING,
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_name_product(CONFIG_PATTERN_STRING_NAME_PRODUCT, d_json)
                #print(text)
            elif self.label[j] == "unit":
                d_json = pytesseract.image_to_data(final_image, lang="vie", config=CONFIG_STRING, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_unit_product(CONFIG_PATTERN_STRING_NAME_UNIT, d_json)
                #print(text)
                #cv2.imwrite("img/unit" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)
            elif self.label[j] == "quantity":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_DECIMAL, \
                                                   output_type=Output.DICT)
                #print("Quality")
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/quantity" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)

            elif self.label[j] == "price":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_DECIMAL, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/price" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)
            elif self.label[j] == "total_price":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_DECIMAL, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/total_price" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)
            elif self.label[j] == "tax":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_NUMBER, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/tax" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)
            elif self.label[j] == "money_tax":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_DECIMAL, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/money_tax" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)

            elif self.label[j] == "total":
                d_json = pytesseract.image_to_data(final_image, config=CONFIG_DECIMAL, \
                                                   output_type=Output.DICT)
                #print(d_json)
                text = post_processing_ocr_price_product(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
                #print(text)
                #cv2.imwrite("img/total" + str(j) + "t_" + str(time.time()) + "_.jpg", final_image)
            if len(text) > 0:
                cv2.rectangle(self.image_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.obj[self.label[j]] = text


def get_start(arr_thread, status):
    for i in range(len(arr_thread)):
        if status == "start":
            arr_thread[i].start()
        if status == "join":
            arr_thread[i].join()
