import cv2

from qlhd.api.utils.pre_processing_util import get_mask_area_color_hsv, draw_multiple_line_straight, \
    find_contours_external
from qlhd.api.utils.util_image import AREA_MIN, AREA_MAX, WIDTH_MIN, WIDTH_MAX, resize


def get_pager(img_origin):
    mask = get_mask_area_color_hsv(img_origin, 200, 255)
    # Sử dụng thuật toán Canny để phát hiện cạnh trong hình ảnh mask.
    edges = cv2.Canny(mask, 1, 150, apertureSize=3)
    draw_line = draw_multiple_line_straight(mask, edges, 1, 10)
    print("draw_line", draw_line)
    if draw_line['error']:
        return draw_line

    contours = find_contours_external(draw_line['mask'])
    x, y, w, h = cv2.boundingRect(contours[0])
    area = w * h
    if AREA_MIN < area < AREA_MAX:
        if WIDTH_MIN < w < WIDTH_MAX:
            roi = img_origin[y:h + y, x:w + x]
            resized = resize(roi)
            return {'error': False, 'message': 'Đã tìm thấy tờ giấy', 'image': resized}
        else:
            return {'error': True, 'message': 'Tờ giấy có width không hợp lệ'}
    else:
        return {'error': True, 'message': 'Không nhận được tờ giấy'}
