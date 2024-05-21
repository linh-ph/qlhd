import cv2
import numpy as np
# from deploy.apps import DeployConfig
from api.src.utils.time_line_util import get_time

def connect_four_angle(image, coordinates):
    # Sắp xếp theo tổng tọa độ x và y
    coordinates_sored = sorted(coordinates, key=lambda obj: obj['sum_x_y'])
    # Lấy top-left và bottom-right
    # obj_start = coordinates_sored[0]
    # obj_end = coordinates_sored[3]
    # cv2.rectangle(image, (obj_start['x'], obj_start['y']), (obj_end['x'] + obj_end['w'], obj_end['y'] + obj_end['h']),
    #               (0, 255, 0), 1)
    return coordinates_sored


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, rect):
    (tl, tr, br, bl) = rect
    #Tính độ dài cạnh bằng pytago lớn nhất làm width và height resize
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))

    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))

    # Tạo các điểm resize mới
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # Thực hiện transform
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (max_width, max_height))

    return warped


def transform_angle(image, coordinates_sored):
    # 4 gốc chia thành 2 dòng sắp xếp theo tọa độ x
    # top-left -> top-right | bottom-right -> bottom-left
    coordinates_row_1 = sorted(coordinates_sored[:2], key=lambda obj: obj['x'])
    coordinates_row_2 = sorted(coordinates_sored[2:], key=lambda obj: obj['x'], reverse=True)
    # merge dòng
    coordinates_table = coordinates_row_1 + coordinates_row_2

    # Lấy tất cả các tọa độ 4 gốc của 1 hình chữ nhật map lại
    pts = []
    for i, c in enumerate(coordinates_table):
        pts.append([[c['x'], c['y']],
                    [c['x'] + c['w'], c['y']],
                    [c['x'], c['y'] + c['h']],
                    [c['x'] + c['w'], c['y'] + c['h']]
                    ])
    # Lấy các gốc lớn nhất của hình chữ nhật
    point_top_left = [pts[0][0][0], pts[0][0][1]]  # point top_left -> top_left -> rectangle 0
    point_top_right = [pts[1][1][0], pts[1][1][1]]  # point top_right -> top_right -> rectangle 1
    point_bottom_right = [pts[2][3][0], pts[2][3][1]]  # point bottom_right -> bottom_right -> rectangle 2
    point_bottom_left = [pts[3][2][0], pts[3][2][1]]  # point bottom_left -> bottom_left -> rectangle 3
    join_coordinates = [point_top_left, point_top_right, point_bottom_right, point_bottom_left]

    # Map các điểm lại thành 1 mảng float
    source_point = np.zeros((4, 2), dtype="float32")
    for i, c in enumerate(join_coordinates):
        source_point[i] = [c[0], c[1]]

    dst = four_point_transform(image, source_point)
    return dst


def draw_prediction(img, idc, i, coordinates, x, y, w, h):
    label = str(idc['classes'][i]) + str(round(idc['confidences'][i], 2))
    coordinates.append({'label': idc['classes'][i],
                        'confidence': round(idc['confidences'][i], 2),
                        'sum_x_y': sum([x, y]),
                        'x': x, 'y': y, 'w': w, 'h': h})
    color = idc['colors'][i]
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(img, str(i), (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 255), 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def get_extra_featured_four_angle(context, image, time_start):
    # Thực hiện đưa ảnh vào model
    # pre = DeployConfig.outs.predict(image, context)
    # if pre['error']:
    #     return pre
    # # Rút trích các đặt trưng của ảnh
    # idc = DeployConfig.outs.indices(image, pre['outs'], context,time_start)
    # if idc['error']:
    #     return idc
    #
    # #Lấy các thông tin đối tượng đã nhận diện
    # coordinates = []
    # for i in idc['indices']:
    #     i = i[0]
    #     box = idc['boxes'][i]
    #     x = abs(round(box[0]))
    #     y = abs(round(box[1]))
    #     w = abs(round(box[2]))
    #     h = abs(round(box[3]))
    #     # Vẽ 4 hình chữ nhật ở 4 gốc
    #     draw_prediction(image, idc, i, coordinates, round(x),
    #                     round(y), round(w), round(h))
    #
    # #Thực hiện các bước kết nối và transform
    # coordinates_sored = connect_four_angle(image, coordinates)
    # image_input = image.copy()
    # image = transform_angle(image, coordinates_sored)
    # cv2.imwrite("img/image_input.jpg", image_input)
    # cv2.imwrite("img/transform_angle.jpg", image)

    return {'error': False, 'message': 'lấy khung giấy success', 'image': image, 'image_input': image_input}
