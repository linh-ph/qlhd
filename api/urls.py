from django.urls import path

from api.src.views.call_store_view import get_data_store_pagination, upload_image_list, \
    get_data_store_detail, get_data_store_update, get_data_store_delete, get_data_store_upload_image_list
from api.src.views.call_axis_view import detected_ocr_create_mask, detected_ocr_save_mask, \
    detected_ocr_update_mask, detected_ocr_list_mask, detected_ocr_delete_mask, export_ocr_csv
from api.src.views.call_home_view import detected_ocr_upload_web, upload_image, export_csv
from api.src.views.call_mobile_view import detected_ocr_upload_mobile_pager_four_angle
from api.src.views.call_session_view import create_session_mobile

urlpatterns = [
    # page home
    path('upload-image', upload_image, name="upload_image"),
    path('detected-web', detected_ocr_upload_web, name="detected_ocr_upload_web"),
    path('csv/<int:id>', export_csv, name='export_csv'),

    # page store
    path('get-data-store-pagination', get_data_store_pagination, name="get_data_store_pagination"),
    path('upload-image-list', upload_image_list, name="upload_image_list"),
    path('get-data-store-detail', get_data_store_detail, name="get_data_store_detail"),
    path('get-data-store-update', get_data_store_update, name="get_data_store_update"),
    path('get-data-store-delete', get_data_store_delete, name="get_data_store_delete"),
    path('get-data-store-upload-image-list', get_data_store_upload_image_list, name="get_data_store_upload_image_list"),

    # page Axis
    path('detected-create-mask', detected_ocr_create_mask, name="detected_ocr_create_mask"),
    path('detected-ocr-save-mask', detected_ocr_save_mask, name="detected_ocr_save_mask"),
    path('detected-ocr-update-mask', detected_ocr_update_mask, name="detected_ocr_update_mask"),
    path('detected-ocr-delete-mask', detected_ocr_delete_mask, name="detected_ocr_delete_mask"),
    path('detected-ocr-list-mask', detected_ocr_list_mask, name="detected_ocr_list_mask"),
    path('export-ocr-csv/<int:id>', export_ocr_csv, name="export_ocr_csv"),

    # mobile
    path('detected-mobile-pager-four-angle', detected_ocr_upload_mobile_pager_four_angle,
         name="detected_ocr_upload_mobile_pager_four_angle"),

    # session
    path('create-session-mobile', create_session_mobile, name="create_session_mobile"),
]

