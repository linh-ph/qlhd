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

# Config Pattern
CONFIG_PATTERN_NUMBER_CODE_BILL = r'[0-9+]{7}'
CONFIG_PATTERN_NUMBER_DATE = r'[0-9+]{2,4}'
CONFIG_PATTERN_STRING_NAME = r'[A-Z]{1,7}'
CONFIG_PATTERN_NUMBER_DECIMAL = r'[0-9+\.]{7}'

# Config Pattern product
CONFIG_PATTERN_STRING_PRODUCT_NAME = r'[a-z+]{1,7}'
CONFIG_PATTERN_STRING_NAME_PRODUCT = r'[aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆ\
fFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTu\
UùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ 0-9+]{1,15}'

CONFIG_PATTERN_STRING_NAME_UNIT = r'[HOP]'

# Config kernel
KERNEL = (17, 8)
KERNEL_MOR = (5, 5)


regex_vie = 'aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆ\
fFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTu\
UùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ'