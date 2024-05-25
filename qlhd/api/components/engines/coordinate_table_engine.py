import cv2

from qlhd.api.assets import TEMPLATE_1_TABLE_PATH, TEMPLATE_2_TABLE_PATH, TEMPLATE_3_TABLE_PATH, TEMPLATE_4_TABLE_PATH, \
    TEMPLATE_5_TABLE_PATH
from qlhd.api.utils.pre_processing_util import get_coordinates_mask


def get_coordinate_table(number_template):
    try:
        template_mask = None
        if number_template == 1:
            template_mask = cv2.imread(TEMPLATE_1_TABLE_PATH)
        elif number_template == 2:
            template_mask = cv2.imread(TEMPLATE_2_TABLE_PATH)
        elif number_template == 3:
            template_mask = cv2.imread(TEMPLATE_3_TABLE_PATH)
        elif number_template == 4:
            template_mask = cv2.imread(TEMPLATE_4_TABLE_PATH)
        elif number_template == 5:
            template_mask = cv2.imread(TEMPLATE_5_TABLE_PATH)
        if template_mask is None:
            return {'error': True, 'message': 'Get coordinate tables fail'}
        else:
            roi_info = get_coordinates_mask(template_mask)
            return {'error': False, 'message': 'Get coordinate success', 'roi_info': roi_info}
    except:
        return {'error': True, 'message': 'Get coordinate tables fail'}
