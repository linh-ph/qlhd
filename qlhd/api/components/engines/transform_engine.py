import cv2
import numpy as np
from imutils.contours import sort_contours

from qlhd.api.assets import TRANSFORM_TEMPLATE_PATH
from qlhd.api.utils.transform_util import find_corner_by_rotated_rect, four_point_transform
from qlhd.api.utils.util_image import resize


def get_container_transform(img_origin):
    try:
        template_mask = cv2.imread(TRANSFORM_TEMPLATE_PATH)
    except:
        return {'error': True, 'message': 'có lỗi khi upload transform_template'}

    gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
    template_mask = cv2.cvtColor(template_mask, cv2.COLOR_BGR2GRAY)
    mask = cv2.bitwise_and(gray, template_mask)

    bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 135], dtype=np.uint8)
    upper_white = np.array([0, 0, 155], dtype=np.uint8)
    get_color = cv2.inRange(hsv, lower_white, upper_white)
    edges = cv2.Canny(mask, 0, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=5, maxLineGap=150)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(get_color, (x1, y1), (x2, y2), (255, 255, 255), 1)

    thresh = cv2.threshold(get_color, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sort_contours(contours, method="top-to-bottom")[0]
    for c in cnts:
        cv2.drawContours(get_color, [c], -1, (255, 255, 255), -1)

    contours, hierarchy = cv2.findContours(get_color, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    approx = cv2.approxPolyDP(contours[0], 0.01 * cv2.arcLength(contours[0], True), True)
    cv2.drawContours(get_color, [approx], -1, (255, 255, 255), -1)
    rect = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rect)

    corner = find_corner_by_rotated_rect(box, approx)
    image = four_point_transform(img_origin, corner)

    if image is not None:
        img_resize = resize(image)
        return {'error': False, 'message': 'get container transform success', 'image': img_resize}
    else:
        return {'error': True, 'message': 'Lỗi không thể container_transform'}
