import cv2

from qlhd.api.assets import TEMPLATE_1_PATH, TEMPLATE_2_PATH, TEMPLATE_3_PATH, TEMPLATE_4_PATH, TEMPLATE_5_PATH
from qlhd.api.utils.pre_processing_util import get_coordinates_mask


def get_coordinate_info(number_template):
    try:
        template_mask = None
        if number_template == 1:
            template_mask = cv2.imread(TEMPLATE_1_PATH)
        elif number_template == 2:
            template_mask = cv2.imread(TEMPLATE_2_PATH)
        elif number_template == 3:
            template_mask = cv2.imread(TEMPLATE_3_PATH)
        elif number_template == 4:
            template_mask = cv2.imread(TEMPLATE_4_PATH)
        elif number_template == 5:
            template_mask = cv2.imread(TEMPLATE_5_PATH)
        if template_mask is None:
            return {'error': True, 'message': 'Lỗi không thể get_coordinate'}
        else:
            roi_info = get_coordinates_mask(template_mask)
            return {'error': False, 'message': 'Get coordinate success', 'roi_info': roi_info}
    except:
        return {'error': True, 'message': 'Lỗi không thể get_coordinate'}
