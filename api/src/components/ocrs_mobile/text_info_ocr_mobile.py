import cv2
import pytesseract
from pytesseract import Output
from api.src.configs import CONFIG_STRING, CONFIG_NUMBER, CONFIG_PATTERN_NUMBER_CODE_BILL, CONFIG_PATTERN_NUMBER_DATE, \
    CONFIG_PATTERN_STRING_NAME, CONFIG_PATTERN_NUMBER_DECIMAL
import time
import re
import numpy as np
import imutils


def post_processing_ocr(pattern, d_json):
    text = ""
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) > 50:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                text = d_json['text'][index]
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break
    return text


def post_processing_ocr_date(pattern, d_json):
    # print(d_json)
    json_text = []
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) > 50:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
                # cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return "/".join(json_text)


def post_processing_ocr_name(pattern, d_json):
    json_text = []
    # print(d_json)
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) > 50:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
    return " ".join(json_text)


def post_processing_ocr_total(pattern, d_json):
    # print(d_json)
    json_text = []
    for index in range(len(d_json['text'])):
        if int(d_json['conf'][index]) > 50:
            if re.match(pattern, d_json['text'][index]):
                (x, y, w, h) = (
                    d_json['left'][index], d_json['top'][index], d_json['width'][index],
                    d_json['height'][index])
                json_text.append(d_json['text'][index])
    return " ".join(json_text)


def get_text_info_mobile(img_origin, image_color, coordinates):
    coordinates_len = len(coordinates)
    label = ["code_bill", "date", "distributor", "total"]
    predictions = []
    for i in range(coordinates_len):
        obj = {}
        x, y, w, h = coordinates[i]
        roi = img_origin[y:y + h, x:x + w]
        now = time.time()
        if i == 0:
            d_json = pytesseract.image_to_data(roi, output_type=Output.DICT)
            text = post_processing_ocr(CONFIG_PATTERN_NUMBER_CODE_BILL, d_json)
            #cv2.imwrite("img/6/roi_info_" + str(now) + ".png", roi)
        elif i == 1:
            # kernel = np.ones((3, 3), dtype=np.uint8)
            # roi = cv2.erode(roi, kernel, iterations=1)
            # roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
            # roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
            d_json = pytesseract.image_to_data(roi, output_type=Output.DICT)
            text = post_processing_ocr_date(CONFIG_PATTERN_NUMBER_DATE, d_json)
            #cv2.imwrite("img/roi_date_" + str(now) + ".png", roi)
        elif i == 2:
            kernel = np.ones((3, 3), dtype=np.uint8)
            roi = cv2.erode(roi, kernel, iterations=1)
            roi = cv2.morphologyEx(roi, cv2.MORPH_OPEN, kernel)
            roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
            d_json = pytesseract.image_to_data(roi, output_type=Output.DICT)
            text = post_processing_ocr_name(CONFIG_PATTERN_STRING_NAME, d_json)
            # cv2.imwrite("img/roi_name_1" + str(now) + ".png", roi)
        else:
            d_json = pytesseract.image_to_data(roi, output_type=Output.DICT)
            text = post_processing_ocr_total(CONFIG_PATTERN_NUMBER_DECIMAL, d_json)
            # print(d_json)
            # cv2.imwrite("img/roi_total_1" + str(now) + ".png", roi)
            # print(text)
        if len(text) > 0:
            cv2.rectangle(image_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
        obj["label"] = label[i]
        obj["x_min"] = x
        obj["y_min"] = y
        obj["x_max"] = x + w
        obj["y_max"] = y + h
        obj["ocr_text"] = text
        predictions.append(obj)
    return predictions
