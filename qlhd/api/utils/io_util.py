from django.core.files.storage import FileSystemStorage


def set_img_to_save(id_img, file_name, file):
    try:
        fs = FileSystemStorage()
        uploaded_file_url = fs.save(id_img + file_name, file)
        full_name = fs.url(uploaded_file_url)
        return {'error': False, 'message': 'Image save success', 'full_name': full_name, 'id_img': id_img}
    except NameError:
        return {'error': True, 'message': 'Hình không thể save'}
