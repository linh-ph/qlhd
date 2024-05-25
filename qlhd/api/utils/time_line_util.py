import time as t
from datetime import datetime


def get_time(title, time_start):
    result = "% 12.2f" % (t.time() - time_start)
    # print(title + ": " + result)
    return str(result).strip()


def convert_date_format(date_str):
    # Định dạng lại ngày để lưu db
    print("date_str", date_str)
    date_str = date_str.replace(' ', '')
    date_str = date_str.strip('_')
    date_str = date_str.replace('Ngày', '')
    date_str = date_str.replace('tháng', '/')
    date_str = date_str.replace('năm', '/')
    date_str = date_str.replace('\n', '')

    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    new_date_str = date_obj.strftime('%Y-%m-%d')
    return new_date_str
