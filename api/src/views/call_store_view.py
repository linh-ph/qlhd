from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time as t
from api.src.utils.io_util import set_img_to_save
from api.src.containers.store import store
import json
from api.models import Image
from django.contrib.auth.models import User
import os
from django.conf import settings


@csrf_exempt
def get_data_store_pagination(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    t_1 = t.time()
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['search'] = body['search']
                data['limit'] = body['limit']
                data['page'] = body['page']
                data['user_id'] = body['user_id']
                data['order_by'] = body['order_by']
            except:
                return JsonResponse(context, status=200)
            # Get URL
            # Get Info From data
            ax = store(data, context, t_1)
            if ax['error']:
                return JsonResponse(context, status=200)

            # # Result
            context['data'] = data
            context['error'] = False
            context['message'] = "Success"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({'error': True, 'message': 'GET'}, status=200)


@csrf_exempt
def upload_image_list(request):
    if request.method == 'POST':
        try:
            file = request.FILES['url']
            if ".jpg" in file.name or ".png" in file.name or ".JPG" in file.name or ".PNG" in file.name:
                user_id = request.POST.get('user_id')

                name_random = str(t.time()) + "_"
                id_img = "capture/" + name_random
                context = set_img_to_save(id_img, file.name, file)
                if not context['error']:

                    # Add to database
                    url = context["full_name"]
                    name = file.name
                    try:
                        u = User.objects.get(pk=user_id)
                        s = Image(url=url, name=name)
                        s.id_user = u
                        s.save()
                    except:
                        context['message'] = "ID không tồn tại"
                        return JsonResponse(context, status=200)
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


@csrf_exempt
def get_data_store_detail(request):
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
            # Get URL
            try:
                s = Image.objects.get(pk=data['id'])
            except Image.DoesNotExist:
                context['message'] = "key không tồn tại"
                return JsonResponse(context, status=200)

            data['url'] = s.url
            data['name'] = s.name
            context['data'] = data
            context['error'] = False
            context['message'] = "Success"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)


@csrf_exempt
def get_data_store_update(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['id'] = body['id']
                data['name'] = body['name']
            except:
                return JsonResponse(context, status=200)
            # Get URL

            url_folder = settings.MEDIA_ROOT + "/capture/"
            url_new = "/media/capture/"

            try:
                s = Image.objects.get(pk=data['id'])

                # Get code random to date
                date_random = s.url.split('/')[-1].split('_')[0] + "_"

                # Rename image
                os.rename(url_folder + date_random + s.name, url_folder + date_random + data['name'])

                # Change url code
                s.url = url_new + date_random + data['name']
                s.name = data['name']
                s.save()
            except Image.DoesNotExist:
                context['message'] = "ID không tồn tại"
                return JsonResponse(context, status=200)

            context['data'] = data
            context['error'] = False
            context['message'] = "Success"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)



@csrf_exempt
def get_data_store_delete(request):
    data = {'error': False}
    context = {"error": True, "message": "Sai tham số"}
    t_1 = t.time()
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['id'] = body['id']
            except:
                return JsonResponse(context, status=200)
            # Get URL


            try:
                s = Image.objects.get(pk=data['id'])
                s.status = False
                s.save()
            except Image.DoesNotExist:
                context['message'] = "ID không tồn tại"
                return JsonResponse(context, status=200)

            context['data'] = data
            context['error'] = False
            context['message'] = "Success"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({"error": False, "message": "API NOT REQUEST METHOD GET"}, status=200)





@csrf_exempt
def get_data_store_upload_image_list(request):
    if request.method == 'POST':
        try:
            file = request.FILES['url']
            if ".jpg" in file.name or ".png" in file.name or ".JPG" in file.name or ".PNG" in file.name:
                id_edit = request.POST.get('id_edit')
                name_random = str(t.time()) + "_"
                id_img = "capture/" + name_random
                context = set_img_to_save(id_img, file.name, file)
                if not context['error']:

                    # Add to database
                    url = context["full_name"]
                    name = file.name
                    try:
                        i = Image.objects.get(pk=id_edit)
                        i.url = url
                        i.name = name
                        i.save()
                    except:
                        context['message'] = "ID không tồn tại"
                        return JsonResponse(context, status=200)
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

