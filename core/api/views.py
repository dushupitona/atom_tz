from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from api.models import OrganizationModel, StorageModel, StorageWasteTypeModel, WasteTypeModel, OrganizationStorageModel,\
    OrganizationWasteValuesModel, OrganizationWasteValuesModel

from api.serializers import OrgListSerializer, OrgRetrieveSerializer, StorageNameSerializer, StorageListSerializer,\
    WasteTypeListSerializer, WasteTypeNameSerializer, OrgStorageSerializer, OrgStorageIntervalSerializer, \
    StorageWasteSerializer, OrgCreateUpdateSerializer, OrgStorageListSerializer, StorageWasteListSerializer,\
    StorageCapasitiesSerializer, OrgWasteValuesSerilaizer


#  <--------------- Organization --------------->
class OrgListAPIView(ListCreateAPIView):
    queryset = OrganizationModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrgListSerializer
        elif self.request.method == 'POST':
            return OrgCreateUpdateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)


class OrgAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OrganizationModel.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrgRetrieveSerializer
        elif self.request.method == 'PUT':
            return OrgCreateUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_200_OK)

#  <--------------- Storage --------------->
class StorageListAPIView(ListCreateAPIView):
    queryset = StorageModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StorageListSerializer
        elif self.request.method == 'POST':
            return StorageNameSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)


class StorageAPIView(RetrieveUpdateDestroyAPIView):
    queryset = StorageModel.objects.all()
    lookup_field = 'id'
    serializer_class = StorageNameSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     data['waste_capacity'] = {}
    #     org_wastes = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=self.kwargs.get('id'))
    #     for waste in org_wastes:
    #         data['waste_capacity'][waste.waste_type.id] = {
    #             'max_capacity': waste.max_capacity,
    #             'max_capacity': waste.current_capacity
    #         }
    #     return Response(data)
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_200_OK)

#  <--------------- Waste --------------->
class WasteTypeListAPIView(ListCreateAPIView):
    queryset = WasteTypeModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WasteTypeListSerializer
        elif self.request.method == 'POST':
            return WasteTypeNameSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)


class WasteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WasteTypeModel.objects.all()
    lookup_field = 'id'
    serializer_class = WasteTypeNameSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_200_OK)


#  <--------------- Org & Storage --------------->
class OrgStorageListAPIView(GenericAPIView):
    queryset = OrganizationStorageModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrgStorageListSerializer
        elif self.request.method == 'POST':
            return OrgStorageSerializer

    def get(self, request, *args, **kwargs):
        queryset = OrganizationStorageModel.objects.select_related('storage').filter(organization=self.kwargs.get('id'))
        serializer=self.get_serializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def post(self, request, *args, **kwargs):
        request.data['organization'] = self.kwargs.get('id')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class OrgStorageAPIView(APIView):
    serializer_class = OrgStorageIntervalSerializer

    def get(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
        serializer = self.serializer_class(instance=org_storage)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def put(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)

        serializer = self.serializer_class(instance=org_storage, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
        org_storage.delete()
        return Response(status=status.HTTP_200_OK)


#  <--------------- Storage & Waste --------------->
class StorageWasteListAPIView(GenericAPIView):
    queryset = OrganizationStorageModel.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StorageWasteListSerializer
        elif self.request.method == 'POST':
            return StorageWasteSerializer

    def get(self, request, *args, **kwargs):
        queryset = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=self.kwargs.get('id'))
        serializer = self.get_serializer(queryset)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def post(self, request, *args, **kwargs):
        request.data['storage'] = self.kwargs.get('id')
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class StorageWasteAPIView(APIView):
    serializer_class = StorageCapasitiesSerializer

    def get(self, request, *args, **kwargs):
        storage_id = self.kwargs.get('storage_id')
        waste_id = self.kwargs.get('waste_id')
        storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)
        serializer = self.serializer_class(storage_waste)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    def put(self, request, *args, **kwargs):
        storage_id = self.kwargs.get('storage_id')
        waste_id = self.kwargs.get('waste_id')
        storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)

        serializer = self.serializer_class(instance=storage_waste, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
    
    def delete(self, request, *args, **kwargs):
        storage_id = self.kwargs.get('storage_id')
        waste_id = self.kwargs.get('waste_id')
        storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)
        storage_waste.delete()
        return Response(status=status.HTTP_200_OK)
    

class OrganizationGenerateAPIView(APIView):
    serializer_class = OrgWasteValuesSerilaizer
    def post(self, request, *args, **kwargs):
        request.data['organization'] = self.kwargs.get('id')
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            waste_value, created = OrganizationWasteValuesModel.objects.get_or_create(organization=data['organization'], waste_type=data['waste_type'], defaults={'value': data['value']})
            if not created:
                waste_value.value += data['value']
                waste_value.save()
            return Response(status=status.HTTP_200_OK)
        print(serializer.errors)


class OrganizationWasteValuesAPIView(APIView):
    def post(self, request, *args, **kwargs):
        organization = self.kwargs.get('id')
        wastes = OrganizationWasteValuesModel.objects.select_related('waste_type').filter(organization=organization)
        waste_values = {waste.waste_type.id: waste.value for waste in wastes}
        print(waste_values)
        
        organization_storages = OrganizationStorageModel.objects.select_related('storage', 'organization').order_by('interval').filter(organization=organization)
        
        for storage in organization_storages:
            storage_wastes = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=storage.storage)
            for waste in storage_wastes:
                if waste.waste_type.id in waste_values.keys():
                    need_eat = waste_values[waste.waste_type.id]
                    if need_eat > 0:
                        eat = need_eat - waste.max_capacity - waste.current_capacity
                        if eat < 0:
                            waste_values[waste.waste_type.id] = 0
                            value = 0
                        else:
                            waste_values[waste.waste_type.id] = eat
                            value = eat

                        org_value = OrganizationWasteValuesModel.objects.get(organization=organization, waste_type=waste.waste_type)
                        waste.current_capacity += abs(eat)
                        waste.save()
                        org_value.value = value
                        org_value.save()
        
        print(waste_values)
        return Response(status=201)
