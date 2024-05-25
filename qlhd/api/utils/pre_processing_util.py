import cv2
import numpy as np
from imutils.contours import sort_contours

RECT_KERNEL = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 7))


# Lấy cạnh
def get_structuring_element(img_origin, kenel_x=1, kenel_y=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kenel_x, kenel_y))
    erosion = cv2.erode(img_origin, kernel, iterations=2)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    return dilation


# lấy tọa độ trong mask
def get_coordinates_mask(template_mask):
    template_mask_gray = cv2.cvtColor(template_mask, cv2.COLOR_BGR2GRAY)
    # chuyển đổi hình ảnh xám thành hình ảnh nhị phân,
    # trong đó các pixel có giá trị lớn được đặt thành màu trắng (255)
    # và các pixel có giá trị nhỏ được đặt thành màu đen (0)
    template_thresh = cv2.threshold(template_mask_gray, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # tìm các đường viền trong ảnh nhị phân
    contours = cv2.findContours(template_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts = sort_contours(contours, method="top-to-bottom")[0]
    roi_info = []
    for i, c in enumerate(cnts):
        # (x, y, width, height) tọa độ của hình chữ nhật bao quanh đối tượng
        x, y, w, h = cv2.boundingRect(c)
        roi_info.append([x, y, w, h])
    return roi_info


# lấy màu theo hsv
def get_mask_area_color_hsv(img_origin, hue_lower=0, hue_upper=255):
    # check image gray, tuple shape chứa số lượng hàng, cột
    if len(img_origin.shape) > 2:
        # Chuyển đổi hình ảnh từ màu BGR sang Xám.
        gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_origin
    bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, hue_lower], dtype=np.uint8)
    upper_white = np.array([0, 0, hue_upper], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    return mask


def draw_multiple_line_straight(mask, image_edges, min_line_length=1, max_line_gap=100, width_line=20):
    lines = cv2.HoughLinesP(image_edges, 1, np.pi / 180, 100, min_line_length, max_line_gap)
    if lines is None:
        return {'error': True, 'message': 'HougnlineP không tìm thấy đường thẳng nào'}

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(mask, (x1, y1), (x2, y2), (255, 255, 255), width_line)
    return {'error': False, 'message': 'HougnlineP đã được tìm thấy', 'mask': mask}


def find_contours_external(mask, count_cnt=1):
    contour = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contour_sorted = sorted(contour, key=lambda value: cv2.contourArea(value), reverse=True)[
                     :count_cnt]  # only save the biggest one
    return contour_sorted


def union_rects(a, b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return (x, y, w, h)


def find_rects(src):
    contours, hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    result = []
    for i in range(len(contours)):
        if hierarchy[0][i][3] == -1:
            r = cv2.boundingRect(contours[i])
            result.append(r)

    return result


def find_rect(src):
    rects = find_rects(src)
    if len(rects):
        result = rects[0]
        for i in range(len(rects) - 1):
            result = union_rects(result, rects[i + 1])
        return result
    else:
        return (-1, -1, 0, 0)
