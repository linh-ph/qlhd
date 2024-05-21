import cv2
import pytesseract


def get_text_info(img_origin, coordinates):
    coor_len = len(coordinates)
    label = ["code_bill", "date", "distributor", "total"]
    predictions = []
    for i in range(coor_len):
        obj = {}
        x, y, w, h = coordinates[i]
        roi = img_origin[y:y + h, x:x + w]
        text = pytesseract.image_to_string(roi, lang="vie")
        if len(text) > 0:
            cv2.rectangle(img_origin, (x, y), (x + w, y + h), (0, 255, 0), 2)
        obj["label"] = label[i]
        obj["x_min"] = x
        obj["y_min"] = y
        obj["x_max"] = x + w
        obj["y_max"] = y + h
        obj["ocr_text"] = text
        predictions.append(obj)
    return predictions
