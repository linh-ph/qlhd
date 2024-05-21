# from api.models import Distributor, Session
from qlhd.models import Distributor


def set_to_database_distributor(id_session, url, text_info, url_result):
    try:
        if (text_info is not None):
            # Get Shop Code from URL detected slit ("") and (".")
            if " " in url or "%" in url:
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
                url_path = url_result.replace('media/','')
                try:
                    # s = Session.objects.get(pk=id_session)
                    d = Distributor(shop_code=shop_code, path=path, code_bill=code_bill, date_invoice=date,
                                    name_distributor=distributor,
                                    total_money=total_money, url=url_path)
                    d.id_session = s
                    d.save()
                except:
                    return 0

                return d.id
            else:

                return 0
        else:

            return 0
    except:
        return 0
