import datetime
import os

import cv2

from du_an import settings
from qlhd.api.components.engines.container_engine import get_container
from qlhd.api.components.engines.coordinate_info_engine import get_coordinate_info
from qlhd.api.components.engines.coordinate_table_engine import get_coordinate_table
from qlhd.api.components.engines.pager_engine import get_pager
from qlhd.api.components.engines.resize_engine import get_resize_image
from qlhd.api.components.engines.transform_engine import get_container_transform
from qlhd.api.components.ocrs.text_info_ocr import get_text_info
from qlhd.api.components.ocrs.text_table_ocr import get_text_table
from qlhd.api.components.serializers.distributor_serializer import set_to_database_distributor
from qlhd.api.components.serializers.product_serializer import set_to_database_product
from qlhd.api.utils.time_line_util import get_time
from qlhd.api.utils.util_image import get_detect_template


def do_scan(data, context, image, time_start):
    try:
        # Resize ảnh về 2500x3000
        res = get_resize_image(image)
        if res['error']:
            return res
        data['time_resize'] = get_time("Time Size resize:", time_start)

        # Phát hiện tờ giấy trắng
        pager = get_pager(res['image'])
        if pager['error']:
            return context
        data['time_pager'] = get_time("Time Size pager:", time_start)

        # print("pager", pager['image'])
        # Lấy khung chứa nội dung
        container = get_container(pager['image'])
        if container['error']:
            return container
        data['timer_container'] = get_time("Time Size container:", time_start)

        # print("container", container['image'])
        # # Thực hiện xoay xoay về đúng định dạng
        transform = get_container_transform(container['image'])
        if transform['error']:
            return transform
        data['timer_transform'] = get_time("Time Transform:", time_start)

        # print("transform", transform)
        # print("datadata", data)

        # # Phát hiện loại mẫu(mask)
        number_template = get_detect_template(data['url'])
        if number_template == 0:
            return context
        data['timer_template'] = get_time("Time Size number template:", time_start)
        print("number_template", number_template)

        # # Thực hiện lấy tọa độ trong mẫu(mask 1): gồm các nội dung không nằm trong table
        coordinates_info = get_coordinate_info(number_template)
        if coordinates_info['error']:
            return coordinates_info
        data['timer_coordinates_info'] = get_time("Time Size coordinate info:", time_start)

        # # Lấy tọa độ bảng  trong mẫu
        coordinates_table = get_coordinate_table(number_template)
        if coordinates_table['error']:
            return coordinates_table
        data['timer_coordinates_table'] = get_time("Time Size coordinate_table:", time_start)
        # print("coordinates_table", coordinates_table)

        # Lấy nội dung
        info = get_text_info(transform['image'], coordinates_info['roi_info'])
        # print("thread_text_info", info)
        # # Thực hiện lấy thông tin trong bảng
        table = get_text_table(transform['image'], coordinates_table['roi_info'])
        # print("thread_text_table", table)

        # Gộp thông tin lại
        data['form_json'] = {'info': info, 'table': table}
        # print("---data['form_json']", data)
        # Tạo ảnh lưu vào db
        now = datetime.datetime.now()
        name_img_i = str(now.time()).replace(":", "") + "_invoice.jpg"
        data["url_result"] = "static/" + "invoices/" + name_img_i
        new_image_dir = os.path.join(settings.MEDIA_ROOT, 'invoices')
        new_image_path = os.path.join(new_image_dir, name_img_i)
        os.makedirs(new_image_dir, exist_ok=True)
        cv2.imwrite(new_image_path, image)

        # Thêm vào database
        # print("Thêm vào database")
        data['id_invoice'] = set_to_database_distributor(data['form_json']['info'], data["url_result"])
        data['num_product'] = set_to_database_product(data['form_json']['table'], data['id_invoice'])

        # print("datadatadatadata111", data)

        return data
    except:
        return context
