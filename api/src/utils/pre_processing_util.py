import numpy as np
import cv2
from imutils.contours import sort_contours
RECT_KERNEL = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 7))


# Lấy cạnh
def get_structuring_element(img_origin, kenel_x=1, kenel_y=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kenel_x, kenel_y))
    erosion = cv2.erode(img_origin, kernel, iterations=2)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    return dilation


# Resize ảnh về kích thức fixed w=2500,h=3500
def resize(img_origin):
    return cv2.resize(img_origin, (2500, 3500))


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
        #(x, y, width, height) tọa độ của hình chữ nhật bao quanh đối tượng
        x, y, w, h = cv2.boundingRect(c)
        roi_info.append([x, y, w, h])
    return roi_info


# lấy màu theo hsv
def get_mask_area_color_hsv(img_origin, hue_lower=0, hue_upper=255):
    # check image gray, tuple shape chứa số lượng hàng, cột
    if len(img_origin.shape) > 2:
        #Chuyển đổi hình ảnh từ màu BGR sang Xám.
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


def word_to_boxes(img_origin):
    gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY) if len(img_origin.shape) == 3 else img_origin
    black_hat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, RECT_KERNEL)
    grad_x = cv2.Sobel(black_hat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad_x = np.absolute(grad_x)
    (min_val, max_val) = (np.min(grad_x), np.max(grad_x))
    grad_x = (255 * ((grad_x - min_val) / (max_val - min_val)))
    grad_x = grad_x.astype("uint8")
    grad_x = cv2.morphologyEx(grad_x, cv2.MORPH_CLOSE, RECT_KERNEL)
    #cv2.imwrite("f_" + str(time.time()) + ".png", grad_x)
    return grad_x


def word_find_area_largest(img_origin, grad_x):
    thresh_x = cv2.threshold(img_origin, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh_x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    roi = None
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        if 10 < h < 70:
            roi = img_origin[y:y + h, x:x + w]
            cv2.rectangle(img_origin, (x, y), (w + x, y + h), (0, 255, 0), 1)
    if roi is None:
        roi = np.ones((50, 50), np.uint8)
        roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    final_image = cv2.copyMakeBorder(thresh, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return final_image


