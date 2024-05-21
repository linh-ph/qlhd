from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import time as t
import numpy as np
from api.src.containers.mobile_four_angle import mobile_four_angle
from api.src.utils.time_line_util import get_time

@csrf_exempt
def detected_ocr_upload_mobile_pager_four_angle(request):
    data = {'error': False}
    context = {"error": True, "message": "Có lỗi xảy ra"}
    t_1 = t.time()
    if request.method == 'POST':
        try:
            try:
                # Lấy các tham số từ body
                data['id_user'] = request.POST.get('id_user')
                data['id_session'] = request.POST.get('id_session')
                data['url'] = request.FILES['url'].name
                if ".png" in data['url']:
                    context["message"] = "Chỉ chấp nhận ảnh jpg"
                    return JsonResponse(context, status=200)
            except:
                context["message"] = "Không đọc được yêu cầu"
                return JsonResponse(context, status=200)
            # Giải mã url sang ảnh format opencv
            try:
                read = cv2.imdecode(np.fromstring(request.FILES['url'].read(), np.uint8), cv2.IMREAD_COLOR)
                data["timer_time"] = get_time("Time Size session:", t_1)
                print(data["timer_time"])
            except:
                context["message"] = "Không thể đọc ảnh"
                return JsonResponse(context, status=200)

            # Bắt đầu nhận diện
            mb = mobile_four_angle(data, context, read, t_1)
            if mb['error']:
                return JsonResponse(context, status=200)

            # Trả kết quả
            context['data'] = data
            context['error'] = False
            context['message'] = "Nhận diện thành công"
            return JsonResponse(context, status=200)
        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)
