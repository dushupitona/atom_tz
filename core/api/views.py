from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import StorageModel, WasteTypeModel, OrganizationGenerateWasteModel, OrganizationStorage,\
StorageWasteTypeModel
from api.serializers import StorageSerializer, WasteOperationSerializer


class StorageDetailAPIView(RetrieveAPIView):
    queryset = StorageModel.objects.all()
    serializer_class = StorageSerializer


class StorageListAPIView(APIView):
    def get(self, request):
        my_objects = WasteTypeModel.objects.all()
        ids = [obj.id for obj in my_objects]
        return Response(ids)
    

class GenerateWasteAPIView(APIView):
    def post(self, request):
        serializer = WasteOperationSerializer(data=request.data) # из заголовка брать id компании
        serializer.is_valid()
        print(serializer.errors) if serializer.errors else None
        valid_data = serializer.validated_data
        print(valid_data)

        for waste in valid_data['wastes']:
            OrganizationGenerateWasteModel.objects.create(
                organization=valid_data['organization'].first(),
                waste_type=waste['waste_type'],
                value=waste['value']
            )

        return Response(status=201)
    

class SendWasteAPIView(APIView):
        def post(self, request):
            serializer = WasteOperationSerializer(data=request.data) # из заголовка брать id компании
            serializer.is_valid()
            print(serializer.errors) if serializer.errors else None
            valid_data = serializer.validated_data
            
            org = valid_data['organization']
            wastes = valid_data['wastes']
            print(wastes)

            storages = OrganizationStorage.objects.select_related('organization', 'storage').filter(organization=org.first()).order_by('interval')

            for storage in storages:
                storage_wastes = StorageWasteTypeModel.objects.filter(storage=storage.storage)
                print(f'Storage: {storage.storage}')
                for waste in storage_wastes:
                    for sended_waste in wastes:
                        if sended_waste['waste_type'] == waste.waste_type:
                            if sended_waste['value'] > 0:
                                eat = sended_waste['value'] - waste.capacity
                                if eat < 0:
                                    sended_waste['value'] = 0
                                else:
                                    sended_waste['value'] = eat

            print(wastes)


            return Response(status=201)