from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
import csv
# from api.models import Distributor
from qlhd.models import Distributor
from django.http import HttpResponse
import cv2


def set_img_to_save(id_img, file_name, file):
    try:
        fs = FileSystemStorage()
        uploaded_file_url = fs.save(id_img + file_name, file)
        full_name = fs.url(uploaded_file_url)
        return {'error': False, 'message': 'Image save success', 'full_name': full_name, 'id_img': id_img}
    except NameError:
        return {'error': True, 'message': 'Hình không thể save'}


def get_img_url_to_opencv(url):
    try:
        pil_image = Image.open(url).convert('RGB')
        open_cv_image = np.array(pil_image)
        image = open_cv_image[:, :, ::-1].copy()
        return {'error': False, 'image': image}
    except NameError:
        return {'error': True}


def write_csv(id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="ocr_to_excel.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(
        ['Mã cửa hàng', 'Số đường dẫn', 'Mã hóa đơn', 'Tên nhà phân phối', 'Ngày xuất HD', 'Tên sản phẩm',
         'Đơn vị tính',
         'Số lượng', 'Đơn giá', 'Thành tiền', 'Chiếc khấu', 'Thuế VAT'])
    distributor = Distributor.objects.filter(pk=id)
    for d in distributor:
        shop_code = str(d.shop_code)
        path = str(d.path.replace('(', '').replace(')', '') if d.path is not None else d.path)
        code_bill = "\'" + str(d.code_bill)
        name_distributor = str(d.name_distributor)
        date_invoice = str(d.date_invoice)

        name = ""
        unit = ""
        quantity = ""
        price = ""
        money_tax = ""
        tax = ""
        total = ""
        for p in d.product_set.all():
            name += str(p.name if p.name is not None else "") + "\n"
            unit += str(p.unit if p.unit is not None else "") + "\n"
            quantity += str(p.quantity if p.quantity is not None else "") + "\n"
            price += str(p.price if p.price is not None else "") + "\n"
            money_tax += str(p.money_tax if p.money_tax is not None else "") + "\n"
            tax += str(p.tax if p.tax is not None else "") + "\n"
            total += str(p.total if p.total is not None else "") + "\n"
        writer.writerow([shop_code, path, code_bill, name_distributor, date_invoice, name, unit, quantity, price, total,
                         money_tax, tax])
    return response


def write_csv_info_image(info_image):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="ocr_to_excel.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(
        ['ID', 'label', 'text'])

    for i in info_image:
        id_i = i.id
        label = i.label
        text = i.text

        writer.writerow([id_i, label, text])
    return response


def save_fusion(image_origin, template_mask):
    mask = cv2.imread(template_mask)
    width_origin = image_origin.shape[1]
    height_origin = image_origin.shape[0]
    mask = cv2.resize(mask, (width_origin, height_origin))
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    origin = image_origin.copy()
    fusion = cv2.bitwise_and(mask_gray, origin)
    cv2.imwrite("img/fusion_1.jpg", fusion)
    return fusion
