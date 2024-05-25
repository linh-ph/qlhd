import cv2

from qlhd.api.assets import PAGER_TEMPLATE_PATH
from qlhd.api.utils.pre_processing_util import get_mask_area_color_hsv, get_structuring_element, find_rect
from qlhd.api.utils.util_image import resize


def get_container(img_origin):
    try:
        template_mask = cv2.imread(PAGER_TEMPLATE_PATH)
    except:
        return {'error': True, 'message': 'có lỗi khi upload pager_template'}
    gray = cv2.cvtColor(img_origin, cv2.COLOR_BGR2GRAY)
    template_mask = cv2.cvtColor(template_mask, cv2.COLOR_BGR2GRAY)
    img_origin_and = cv2.bitwise_and(gray, template_mask)
    get_color = get_mask_area_color_hsv(img_origin_and, 135, 155)
    blur = cv2.GaussianBlur(get_color, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.THRESH_BINARY_INV | cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 31, 10)
    thresh = 255 - thresh

    h_origin, w_origin = get_color.shape
    vertical = get_structuring_element(thresh, 1, int(h_origin / 50))
    horizontal = get_structuring_element(thresh, int(w_origin / 50), 1)
    mask = vertical + horizontal

    x, y, w, h = find_rect(mask)
    img_origin = img_origin[y:y + h, x:x + w]
    if img_origin is not None:
        roi = resize(img_origin)
        return {'error': False, 'message': 'lấy khung giấy success', 'image': roi}
    else:
        return {'error': True, 'message': 'Không tìm được hình khung tờ giấy'}
