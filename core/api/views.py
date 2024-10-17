from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.models import StorageModel
from api.serializers import StorageSerializer

class StorageDetailAPIView(RetrieveAPIView):
    queryset = StorageModel.objects.all()
    serializer_class = StorageSerializer


class StorageListAPIView(ListAPIView):
    queryset = StorageModel.objects.all()
    serializer_class = StorageSerializer
    