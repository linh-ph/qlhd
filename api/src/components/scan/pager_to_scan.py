from skimage.filters import threshold_local
from skimage import img_as_ubyte
import cv2


def get_pager_to_scan(image_origin, context):
    try:
        # Chuyển ảnh xám
        gray = cv2.cvtColor(image_origin, cv2.COLOR_BGR2GRAY)
        # # Nhị phân ảnh skimage
        adaptive_thresh = threshold_local(gray, 75, offset=10)
        # # convert adapter_thresh
        binary_adaptive = gray > adaptive_thresh
        image = img_as_ubyte(binary_adaptive)
        return {"error": False, "image": image}
    except:
        context['message'] = "Không thể convert scikit-image to opencv"
        return context


def resize_mask_to_image(image_origin, path):
    mask = cv2.imread(path)
    width_origin = image_origin.shape[1]
    height_origin = image_origin.shape[0]

    return cv2.resize(mask, (width_origin, height_origin))
