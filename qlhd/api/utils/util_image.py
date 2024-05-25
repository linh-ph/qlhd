import cv2

# config pager
AREA_MIN = 7000000
AREA_MAX = 10000000
WIDTH_MIN = 2000
WIDTH_MAX = 3000

# Config OCR
ROW_SIZE = 8
CONFIG_NUMBER = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789 outputbase digits'
CONFIG_DECIMAL = '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789.,'
CONFIG_STRING = '--psm 6 --oem 3'
CONFIG_STRING_SINGE_CHAR = '--psm 6 --oem 3'
# Config kernel
KERNEL = (17, 8)
KERNEL_MOR = (5, 5)


# Resize ảnh về kích thức fixed w=2500,h=3500
def resize(img_origin):
    return cv2.resize(img_origin, (2500, 3500))


def convert_string_to_float(s):
    # 00.000,00 -> 00000.00
    try:
        print("s", s)
        if not s:
            return 0
        s = s.replace('.', '')
        s = s.replace(',', '.')
        return float(s)
    except:
        return 0


def get_detect_template(url):
    number_template = 0
    url = url.lower()
    if "(85)" in url:
        number_template = 1
    if "(91)" in url:
        number_template = 2
    if "(95)" in url:
        number_template = 3
    if "(99)" in url:
        number_template = 4
    if "(100)" in url:
        number_template = 5

    return number_template
