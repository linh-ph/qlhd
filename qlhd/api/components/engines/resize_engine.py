from qlhd.api.utils.util_image import resize


def get_resize_image(img_origin):
    if img_origin is not None:
        img_read = resize(img_origin)
        return {'error': False, 'message': 'Image resize success', 'image': img_read}
    else:
        return {'error': True, 'message': 'Image không thể resize'}
