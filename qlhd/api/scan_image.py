import time as t

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from skimage import io

from qlhd.api.components.get_scan import do_scan
from qlhd.api.utils.io_util import set_img_to_save


@csrf_exempt
def detected_ocr_upload_image(request):
    data = {'error': False}
    context = {'error': True, "message": "Image Invalid"}
    t_1 = t.time()
    if request.method == 'POST':
        try:
            try:
                data['url'] = request.POST.get('url')
            except:
                context["message"] = "Không tồn tại id_folder và url"
                return JsonResponse(context, status=200)

            read = io.imread(settings.IP_SITE + data['url'])
            if read is None:
                context['message'] = "ảnh không tồn tại"
                return JsonResponse(context, status=200)

            print("read", read)
            # Start Handle
            _scan = do_scan(data, context, read, t_1)
            if _scan['error']:
                return JsonResponse(context, status=400)

            # Result
            context['data'] = data
            context['error'] = False
            context['message'] = "Hình đã xử lí xong"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=400)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.POST.get('id_img'):
        try:
            file = request.FILES['url']
            if ".jpg" in file.name or ".png" in file.name or ".JPG" in file.name or ".PNG" in file.name:
                id_img = request.POST.get('id_img')
                context = set_img_to_save(id_img, file.name, file)
                if not context['error']:
                    return JsonResponse(context, status=200)
                else:
                    return JsonResponse(context, status=400)
            else:
                return JsonResponse({'error': True, 'message': 'Ảnh không đúng format'}, status=400)

        except NameError:
            return JsonResponse({'error': True, 'message': 'Có lỗi xảy ra'}, status=400)

    else:
        context = {
            'error': True,
            'message': 'Request Fail',
        }
        return JsonResponse(context, status=401)
