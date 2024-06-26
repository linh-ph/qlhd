from qlhd.api.utils.thread_util import MyThread, get_start


def get_text_table(img_origin, coordinates):
    i_index = 1
    len_coordinates = len(coordinates)
    arr_coordinates = []
    arr_row = []
    for i in range(len_coordinates):
        if i_index != 8:
            arr_row.append(coordinates[i])
            i_index = i_index + 1
        else:
            arr_row.append(coordinates[i])
            arr_coordinates.append(arr_row)
            arr_row = []
            i_index = 1

    label = ["name", "unit", "quantity", "price", "total_price", "tax", "tax_money", "total"]
    predictions = []
    arr_thread = []

    for i in range(len(arr_coordinates)):
        thr = MyThread(arr_coordinates[i], img_origin, label)
        arr_thread.append(thr)

    get_start(arr_thread, "start")
    get_start(arr_thread, "join")

    for i in range(len(arr_thread)):
        predictions.append(arr_thread[i].obj)
    return predictions
