from django.http import HttpResponse
from django.http import JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def upload_image(request):
#     if request.method == 'POST' and request.POST.get('id_img'):
#         try:
#             file = request.FILES['url']
#             if ".jpg" in file.name or ".png" in file.name or ".JPG" in file.name or ".PNG" in file.name:
#                 id_img = request.POST.get('id_img')
#                 context = set_img_to_save(id_img, file.name, file)
#                 if not context['error']:
#                     return JsonResponse(context, status=200)
#                 else:
#                     return JsonResponse(context, status=400)
#             else:
#                 return JsonResponse({'error': True, 'message': 'Ảnh không đúng format'}, status=400)
#
#         except NameError:
#             return JsonResponse({'error': True, 'message': 'Có lỗi xảy ra'}, status=400)
#
#     else:
#         context = {
#             'error': True,
#             'message': 'Request Fail',
#         }
#         return JsonResponse(context, status=401)
