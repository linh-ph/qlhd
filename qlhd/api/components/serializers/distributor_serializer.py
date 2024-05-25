from qlhd.api.utils.time_line_util import convert_date_format
from qlhd.models import Distributor, Invoice


def set_to_database_distributor(text_info, url_result):
    if text_info is not None:
        code_bill = text_info[0]['ocr_text']
        date = text_info[1]['ocr_text']
        distributor_name = text_info[2]['ocr_text']
        total_money = text_info[3]['ocr_text']
        # url_path = url_result.replace('static/', '')

        try:
            d = Distributor(name=distributor_name)
            d.save()

            invoice = Invoice(
                code_bill=code_bill,
                date_invoice=convert_date_format(date),
                total_money=total_money,
                image_path=url_result,
                distributor=d)
            invoice.save()

        except:
            return 0

        return invoice.id
    else:
        return 0
