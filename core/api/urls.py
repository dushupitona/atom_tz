from django.contrib import admin
from django.urls import path, include

from api.views import OrgListAPIView, OrgAPIView, StorageListAPIView, StorageAPIView,\
    WasteAPIView, WasteTypeListAPIView, OrgStorageListAPIView, OrgStorageAPIView,\
    OrgStorageListAPIView, StorageWasteListAPIView


app_name = 'api'

urlpatterns = [
    path('org/', OrgListAPIView.as_view()),
    path('org/<int:id>/', OrgAPIView.as_view()),
    
    path('org/<int:id>/storage/', OrgStorageListAPIView.as_view()),
    path('org/<int:org_id>/storage/<int:storage_id>/', OrgStorageAPIView.as_view()),


    path('storage/', StorageListAPIView.as_view()),
    path('storage/<int:id>/', StorageAPIView.as_view()),
    
    path('waste/', WasteTypeListAPIView.as_view()),
    path('waste/<int:id>/', WasteAPIView.as_view()),

    path('storage/<int:id>/waste/', StorageWasteListAPIView.as_view()),
    # path('org/<int:org_id>/storage/<int:storage_id>/', OrgStorageAPIView.as_view()),
]
