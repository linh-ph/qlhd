from qlhd.models import Distributor, Invoice
from datetime import datetime


def convert_date_format(date_str):
    # Định dạng lại ngày để lưu db
    date_str = date_str.replace(' ', '')
    date_str = date_str.replace('_Ngày', '')
    date_str = date_str.replace('tháng', '/')
    date_str = date_str.replace('năm', '/')
    date_str = date_str.replace('\n', '')

    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    new_date_str = date_obj.strftime('%Y-%m-%d')
    return new_date_str


def set_to_database_distributor(url, text_info, url_result):
    if text_info is not None:
        # Get Shop Code from URL detected slit ("") and (".")
        # if " " in url or "%" in url:
        #     s = ""
        #     if " " in url:
        #         s = url.split()
        #     if "%20" in url:
        #         s = url.split("%20")
        #     path_url = s[0].split("/")
        #     path = s[1].split(".")[0]
        #
        # else:
        #     return 0
        code_bill = text_info[0]['ocr_text']
        date = text_info[1]['ocr_text']

        distributor_name = text_info[2]['ocr_text']
        total_money = text_info[3]['ocr_text']
        url_path = url_result.replace('media/', '')

        try:
            # s = Session.objects.get(pk=id_session)
            d = Distributor(name=distributor_name)
            d.save()

            invoice = Invoice(
                code_bill=code_bill,
                date_invoice=convert_date_format(date),
                total_money=total_money,
                image_path=url_path,
                distributor=d)
            invoice.save()
        except:
            return 0

        return d.id
    else:
        return 0
