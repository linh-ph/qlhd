from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from api.models import Session
from django.contrib.auth.models import User
import os

@csrf_exempt
def create_session_mobile(request):
    data = {'error': False}
    context = {"error": True, "message": "Chưa nhận đủ tham số"}
    if request.method == 'POST':
        try:
            try:
                # get params is body
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                data['id_user'] = body['id_user']
                data['folder'] = body['folder']
            except:
                return JsonResponse(context, status=200)
            # Get Info From data
            create_folder = "media/" + str(data['folder']) + "/"

            # try:
            #     u = User.objects.get(id=data['id_user'])
            #     s = Session(folder=data['folder'])
            #     s.id_user = u
            #     s.save()
            #     data['id_session'] = s.id
            # except:
            #     context['message'] = "Không tìm thấy user"
            #     return JsonResponse(context, status=200)

            # Nếu đã tồn tại thì không tạo nữa
            try:
                os.mkdir(create_folder)
            except OSError as error:
                context['message'] = "Thư mục đã có"
                return JsonResponse(context, status=200)

            data['path'] = create_folder
            context['data'] = data
            context['error'] = False
            context['message'] = "Tạo thành công"
            return JsonResponse(context, status=200)

        except NameError:
            return JsonResponse(context, status=200)
    else:
        return JsonResponse({'error': True, 'message': 'GET'}, status=200)
