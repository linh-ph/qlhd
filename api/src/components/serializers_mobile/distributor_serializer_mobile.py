# from api.models import Distributor, Session
from qlhd.models import Distributor


def set_to_database_distributor(id_session, url, url_result, text_info, context):
    if " " in url or "%" in url:
        try:
            s = ""
            if " " in url:
                s = url.split()
            if "%20" in url:
                s = url.split("%20")
            path_url = s[0].split("/")
            shop_code = path_url[-1]
            path = s[1].split(".")[0]
            code_bill = text_info[0]['ocr_text']
            date = text_info[1]['ocr_text']
            distributor = text_info[2]['ocr_text']
            total_money = text_info[3]['ocr_text']
            # s = Session.objects.get(pk=id_session)
            d = Distributor(shop_code=shop_code, path=path, code_bill=code_bill, date_invoice=date,
                            name_distributor=distributor,
                            total_money=total_money, url=url_result.replace('media/', ''))
            # d.id_session = s
            d.save()
            return {'error': False, 'id_distributor': d.id}
        except:
            context['message'] = "Có lỗi xảy ra thi thêm vào bảng distributor"
            return context

    else:
        context['message'] = "url không đúng format"
        return context
