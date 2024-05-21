import cv2
from imutils.contours import sort_contours


# lấy tọa độ trong mask
def get_coordinate_info(template_mask):
    template_mask_gray = cv2.cvtColor(template_mask, cv2.COLOR_BGR2GRAY)
    template_thresh = cv2.threshold(template_mask_gray, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(template_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sort_contours(contours, method="top-to-bottom")[0]
    return [cv2.boundingRect(c) for c in contours]
