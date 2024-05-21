import cv2
import pytesseract
from api.src.utils.time_line_util import get_time
from api.src.configs import CONFIG_STRING


def axis(data, context, image, time_start):
    # Lấy các thông tin cần thiết ra gồm khung và tọa độ đã xác định trên khung
    coordinates = data['coordinates'][0]
    x_min = coordinates['x']
    y_min = coordinates['y']
    x_max = coordinates['x'] + coordinates['w']
    y_max = coordinates['y'] + coordinates['h']

    try:
        roi = image[y_min:y_max, x_min: x_max]
    except:
        context['message'] = "Không thể cắt vùng ảnh"
        return context

    # Tiền sử lí ảnh
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    final_image = cv2.copyMakeBorder(thresh, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))

    # đọc vùng đã set
    text = pytesseract.image_to_string(final_image, lang="vie", config=CONFIG_STRING)
    # Thêm text vào vùng mảng
    export = []
    obj_info = {
        "label": "chưa có lable",
        "text": text,
        "xmin": x_min,
        "ymin": y_min,
        "xmax": x_max,
        "ymax": y_max,
    }
    export.append(obj_info)
    data['export'] = export
    data["timer_axis"] = get_time("Time Size:", time_start)
    return data
