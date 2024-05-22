from django.urls import path

from api.src.views.call_axis_view import detected_ocr_create_mask, detected_ocr_save_mask, \
    detected_ocr_update_mask, detected_ocr_list_mask, detected_ocr_delete_mask, export_ocr_csv
from api.src.views.call_home_view import detected_ocr_upload_web, upload_image, export_csv
from api.src.views.call_session_view import create_session_mobile

urlpatterns = [
    # page home
    path('upload-image', upload_image, name="upload_image"),
    path('detected-web', detected_ocr_upload_web, name="detected_ocr_upload_web"),
    path('csv/<int:id>', export_csv, name='export_csv'),

    # page Axis
    # path('detected-create-mask', detected_ocr_create_mask, name="detected_ocr_create_mask"),
    # path('detected-ocr-save-mask', detected_ocr_save_mask, name="detected_ocr_save_mask"),
    # path('detected-ocr-update-mask', detected_ocr_update_mask, name="detected_ocr_update_mask"),
    # path('detected-ocr-delete-mask', detected_ocr_delete_mask, name="detected_ocr_delete_mask"),
    # path('detected-ocr-list-mask', detected_ocr_list_mask, name="detected_ocr_list_mask"),
    # path('export-ocr-csv/<int:id>', export_ocr_csv, name="export_ocr_csv"),


    # session
    path('create-session-mobile', create_session_mobile, name="create_session_mobile"),
]

