import cv2
import datetime
from threading import Thread
from queue import Queue
from api.src.components.yolo.extra_featured_four_angle import get_extra_featured_four_angle
from api.src.utils.time_line_util import get_time
from api.src.components.scan.pager_to_scan import get_pager_to_scan, resize_mask_to_image
from api.src.components.coordinates.get_coordinate_info import get_coordinate_info
from api.src.components.coordinates.get_coordinate_table import get_coordinate_table
from api.src.components.ocrs_mobile.text_info_ocr_mobile import get_text_info_mobile
from api.src.components.ocrs_mobile.text_table_ocr_mobile import get_text_table_mobile
# from api.models import Session
from api.src.components.serializers_mobile.distributor_serializer_mobile import set_to_database_distributor
from api.src.components.serializers_mobile.product_serializer_mobile import set_to_database_product
from api.src.assets import TEMPLATE_INFO_PATH, TEMPLATE_TABLE_PATH


def mobile_four_angle(data, context, image, time_start):
    # Lấy đặt trưng từ ảnh để xác định có hóa đơn hay không.
    featured = get_extra_featured_four_angle(context, image, time_start)
    if featured['error']:
        return featured
    data["timer_yolo"] = get_time("Time Size session:", time_start)
    # Bắt đầu tiền xử lý

    # Phân ngưỡng threshold local
    scan = get_pager_to_scan(featured['image'], context)
    if scan['error']:
        return scan
    data["timer_scan"] = get_time("Time Size scan:", time_start)
    # End tiền xử lí ảnh.

    # Start Ocr Engines
    # Copy ra 1 ảnh màu để vẽ viền
    image_color = cv2.cvtColor(scan['image'], cv2.COLOR_GRAY2BGR)
    # Resize mask == image
    mask_info = resize_mask_to_image(scan['image'], TEMPLATE_INFO_PATH)
    mask_table = resize_mask_to_image(scan['image'], TEMPLATE_TABLE_PATH)
    #cv2.imwrite("img/mask.png", mask_table)
    # Lấy các tọa độ trong mask
    coordinates_info = get_coordinate_info(mask_info)
    coordinates_table = get_coordinate_table(mask_table)
    data["timer_load_mask"] = get_time("Time Size timer_load_mask:", time_start)

    # Tạo hàng đợi
    que1 = Queue()
    que2 = Queue()

    # Lấy nội dung
    thread_text_info = Thread(target=lambda q, arg1, arg2, arg3: q.put(get_text_info_mobile(arg1, arg2, arg3)),
                              args=(que1, scan['image'], image_color, coordinates_info))

    # Thực hiện lấy thông tin trong bảng
    thread_text_table = Thread(target=lambda q, arg1, arg2, arg3: q.put(get_text_table_mobile(arg1, arg2, arg3)),
                               args=(que2, scan['image'], image_color, coordinates_table))

    # Bắt đầu Thread
    thread_text_info.start()
    thread_text_table.start()

    # Thread nào xong trước thì đợi ở đây.
    thread_text_info.join()
    thread_text_table.join()
    data["timer_thread"] = get_time("Time Size timer_thread:", time_start)

    # Gộp thông tin lại
    data['form_json'] = {'info': que1.get(), 'table': que2.get()}
    # End Ocr Engines
    # try:
    #     # Lấy folder session
    #     # s = Session.objects.get(pk=data['id_session'])
    #     data['folder'] = s.folder
    # except:
    #     context['message'] = "session không tồn tại"
    #     return context
    now = datetime.datetime.now()
    path_image_ori = data['folder'] + "/" + str(now) + "_origin_form.jpg"
    data["url_result_color"] = "media/" + path_image_ori

    cv2.imwrite(data["url_result_color"], image_color)

    # Bắt đầu thêm vào database
    distributor = set_to_database_distributor(data['id_session'], data['url'], data['url_result_color'],
                                              data['form_json']['info'], context)
    if distributor['error']:
        return distributor

    product = set_to_database_product(data['form_json']['table'], distributor['id_distributor'], context)
    if product['error']:
        return product
    data['info_distributor'] = distributor
    data['info_product'] = product

    data["timer_add_database_final"] = get_time("Time Size timer_add_database:", time_start)

    # End thêm vào database
    return data
