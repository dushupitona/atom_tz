from django.urls import path

from api.views import OrgListAPIView, OrgAPIView, StorageListAPIView, StorageAPIView,\
    WasteAPIView, WasteTypeListAPIView, OrgStorageListAPIView, OrgStorageAPIView,\
    OrgStorageListAPIView, StorageWasteListAPIView, StorageWasteAPIView, OrgGenerateAPIView,\
    OrgSendAPIView

app_name = 'api'

urlpatterns = [
    path('org/', OrgListAPIView.as_view(), name='org'),
    path('org/<int:id>/', OrgAPIView.as_view(), name='org_object'),
    
    path('org/<int:id>/storage/', OrgStorageListAPIView.as_view(), name='org_storage'),
    path('org/<int:org_id>/storage/<int:storage_id>/', OrgStorageAPIView.as_view(), name='org_storage_object'),

    path('org/<int:id>/generate/', OrgGenerateAPIView.as_view(), name='org_generate'),
    path('org/<int:id>/send/', OrgSendAPIView.as_view(), name='org_send'),


    path('storage/', StorageListAPIView.as_view(), name='storage'),
    path('storage/<int:id>/', StorageAPIView.as_view(), name='storage_object'),
    

    path('waste/', WasteTypeListAPIView.as_view(), name='waste'),
    path('waste/<int:id>/', WasteAPIView.as_view(), name='waste_object'),


    path('storage/<int:id>/waste/', StorageWasteListAPIView.as_view(), name='storage_waste'),
    path('storage/<int:storage_id>/waste/<int:waste_id>/', StorageWasteAPIView.as_view(), name='storage_waste_object'),
]
