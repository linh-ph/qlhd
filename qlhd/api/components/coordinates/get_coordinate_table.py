import cv2


# lấy tọa độ trong mask
def get_coordinate_table(template_mask):
    template_mask_gray = cv2.cvtColor(template_mask, cv2.COLOR_BGR2GRAY)
    template_thresh = cv2.threshold(template_mask_gray, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(template_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    sored_y = sorted(contours, key=lambda x: x[0, 0, 1])
    cnt_3 = []
    step = 8
    len_cnt_y = len(sored_y)
    row = 1
    # step * row = start của 1 dòng
    # start + row = end vị trí kết thúc 1 dòng
    for i in range(0, len_cnt_y, step):
        if i == 0:
            cnt = sorted(sored_y[:step], key=lambda x: x[0, 0, 0])
        else:
            start = step * row
            end = start + step
            cnt = sorted(sored_y[start:end], key=lambda x: x[0, 0, 0])
        cnt_3 = cnt_3 + cnt
    return [cv2.boundingRect(c) for c in cnt_3]
