from django.contrib import admin
from django.urls import path, include

from api.views import StorageDetailAPIView, StorageListAPIView,\
      GenerateWasteAPIView, SendWasteAPIView


app_name = 'api'

urlpatterns = [
    path('storage/<int:pk>/', StorageDetailAPIView.as_view()),
    path('storage/', StorageListAPIView.as_view()),
    path('generate/', GenerateWasteAPIView.as_view()),
    path('send/', SendWasteAPIView.as_view()),
]
