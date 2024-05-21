from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from skimage import io
import time as t
import cv2
from django.conf import settings
import json
from api.src.containers.axis import axis
from api.models import Image, InfoImage
from api.src.utils.io_util import write_csv_info_image


@csrf_exempt
def detected_ocr_create_mask(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số truyền lên"}
    t_1 = t.time()
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['img_info'] = body['img_info']
                data['coordinates'] = body['data']
            except:
                return JsonResponse(context, status=200)
            # Get URL
            try:
                read = io.imread(settings.IP_SITE + data['img_info']['url'].replace(' ', '%20'))

            except:
                context["message"] = "Không thể đọc ảnh"
                return JsonResponse(context, status=200)
            # Get Info From data
            read = cv2.cvtColor(read, cv2.COLOR_BGR2RGB)
            ax = axis(data, context, read, t_1)
            if ax['error']:
                return JsonResponse(context, status=200)

            # # Result

            context['data'] = data
            context['error'] = False
            context['message'] = "Ảnh đã đúng"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def detected_ocr_update_mask(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['info'] = body['data']
                data['id'] = body['id']
            except:
                return JsonResponse(context, status=200)
            # Lấy các thông tin ra
            info = data['info']

            # Insert
            try:
                i = InfoImage.objects.get(pk=data['id'])
                i.label = info['label']
                i.text = info['text']
                i.save()
            except:
                context['message'] = "Không tìm thấy ID"
                return JsonResponse(context, status=200)

            # # Result

            context['data'] = data
            context['error'] = False
            context['message'] = "Thêm thành công"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def detected_ocr_save_mask(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['info'] = body['data']
                data['id'] = body['id']
            except:
                return JsonResponse(context, status=200)
            # Lấy các thông tin ra
            info = data['info']
            try:
                s = Image.objects.get(pk=data['id'])
                i = InfoImage(label=info['label'], text=info['text'])
                i.id_image = s
                i.save()
            except:
                context['message'] = "ID không tồn tại"
                return JsonResponse(context, status=200)
            # Insert

            data['id_new'] = i.id
            # # Result
            context['data'] = data
            context['error'] = False
            context['message'] = "Thêm thành công"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def detected_ocr_list_mask(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['id'] = body['id']
                data['order_by'] = body['order_by']
            except:
                return JsonResponse(context, status=200)

            # Lấy các thông tin ra
            try:
                # có sắp xếp hay không (-) là sắp xếp giảm dần
                order_by = "" if data['order_by'] == "asc" else "-"

                # Thực hiện select .filter(status="0")
                i = InfoImage.objects.all().filter(id_image=data['id'], status="1").order_by(order_by + 'id')
                c = InfoImage.objects.filter(id_image=data['id'], status="1").count()

                # Nếu có dư thì thêm 1 page
                data['image'] = list(i.values())
                data['total_count'] = c
            except:
                context['message'] = "ID không tồn tại"
                return JsonResponse(context, status=200)
            # Insert
            arr = []
            for row in range(c):
                obj = {'label': i[row].label, 'text': i[row].text}
                arr.append(obj)

            context['data'] = data
            context['format_json'] = json.dumps(arr, indent=4, separators=(", ", " : "))
            context['error'] = False
            context['message'] = "Thêm thành công"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def detected_ocr_delete_mask(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['id'] = body['id']
            except:
                return JsonResponse(context, status=200)
            # Lấy các thông tin ra

            # Insert
            try:
                i = InfoImage.objects.get(pk=data['id'])
                i.status = False
                i.save()
            except:
                context['message'] = "Không tìm thấy ID"
                return JsonResponse(context, status=200)

            context['data'] = data
            context['error'] = False
            context['message'] = "Thêm thành công"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def export_ocr_csv(request, id):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'GET':
        try:
            data['id'] = id
            data['order_by'] = 'asc'
            # Lấy các thông tin ra
            try:
                order_by = "" if data['order_by'] == "asc" else "-"
                info_image = InfoImage.objects.all().filter(id_image=data['id'], status="1").order_by(order_by + 'id')
            except:
                context['message'] = "ID không tồn tại"
                return JsonResponse(context, status=200)
            return write_csv_info_image(info_image)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD POST"}, status=200)
