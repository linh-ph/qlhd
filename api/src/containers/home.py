import cv2
from threading import Thread
from queue import Queue
import datetime
from api.src.utils.time_line_util import get_time

from api.src.components.engines.resize_engine import get_resize_image
from api.src.components.engines.pager_engine import get_pager

from api.src.components.engines.container_engine import get_container
from api.src.components.engines.transform_engine import get_container_transform
from api.src.components.engines.detect_template_engine import get_detect_template
from api.src.components.engines.coordinate_info_engine import get_coordinate_info
from api.src.components.engines.coordinate_table_engine import get_coordinate_table

from api.src.components.ocrs.text_info_ocr import get_text_info
from api.src.components.ocrs.text_table_ocr import get_text_table
from api.src.components.serializers.distributor_serializer import set_to_database_distributor
from api.src.components.serializers.product_serializer import set_to_database_product


def home(data, context, image, time_start):
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

        # # Lấy lấy khung chứa nội dung
        container = get_container(pager['image'])
        if container['error']:
            return container
        data['timer_container'] = get_time("Time Size container:", time_start)

        #
        # # Thực hiện xoay xoay về đúng định dạng
        transform = get_container_transform(container['image'])
        if transform['error']:
            return transform
        data['timer_transform'] = get_time("Time Transform:", time_start)

        #
        # # Phát hiện loại mẫu(mask)
        number_template = get_detect_template(data['url'])
        if number_template == 0:
            return context
        data['timer_template'] = get_time("Time Size number template:", time_start)
        #
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

        # Create Que
        que1 = Queue()
        que2 = Queue()
        # Lấy nội dung
        thread_text_info = Thread(target=lambda q, arg1, arg2: q.put(get_text_info(arg1, arg2)),
                                  args=(que1, transform['image'], coordinates_info['roi_info']))

        # # Thực hiện lấy thông tin trong bảng
        thread_text_table = Thread(target=lambda q, arg1, arg2: q.put(get_text_table(arg1, arg2)),
                                   args=(que2, transform['image'], coordinates_table['roi_info']))

        thread_text_info.start()
        thread_text_table.start()

        thread_text_info.join()
        thread_text_table.join()

        # Gộp thông tin lại
        data['form_json'] = {'info': que1.get(), 'table': que2.get()}
        # Lấy url ảnh ngẫu nhiên.
        now = datetime.datetime.now()
        data["url_result"] = "media/" + data['id_session'] + "/" + str(now) + "_form.jpg"
        # Thêm vào database
        data['id_late'] = set_to_database_distributor(data['id_session'], data['url'], data['form_json']['info'], data["url_result"])
        data['num_product'] = set_to_database_product(data['form_json']['table'], data['id_late'])
        data['timer_final'] = get_time("Time Size thread final:", time_start)


        cv2.imwrite(data["url_result"], transform['image'])
        data['timer_create_session'] = get_time("Time Size session:", time_start)
        return data
    except:
        return context
