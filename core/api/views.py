from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import serializers

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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class OrgAPIView(RetrieveUpdateDestroyAPIView):
    queryset = OrganizationModel.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrgRetrieveSerializer
        elif self.request.method == 'PUT':
            return OrgCreateUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class StorageAPIView(RetrieveUpdateDestroyAPIView):
    queryset = StorageModel.objects.all()
    lookup_field = 'id'
    serializer_class = StorageNameSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({'detail': 'Хранилище не найдено.'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Хранилище не найдено.'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Хранилище не найдено.'}, status=status.HTTP_404_NOT_FOUND)

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
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class WasteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = WasteTypeModel.objects.all()
    lookup_field = 'id'
    serializer_class = WasteTypeNameSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({'detail': 'Вид отхода не найден.'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Вид отхода не найден.'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        try:
            self.perform_destroy(self.get_object())
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Вид отхода не найден.'}, status=status.HTTP_404_NOT_FOUND)


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
        if queryset:
            serializer=self.get_serializer(queryset)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['organization'] = self.kwargs.get('id')
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)


class OrgStorageAPIView(APIView):
    serializer_class = OrgStorageIntervalSerializer

    def get(self, request, *args, **kwargs):
        try:
            org_id = self.kwargs.get('org_id')
            storage_id = self.kwargs.get('storage_id')
            org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
            serializer = self.serializer_class(instance=org_storage)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return Response({'detail': 'Объект не найден.'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        try:
            org_id = self.kwargs.get('org_id')
            storage_id = self.kwargs.get('storage_id')
            org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
            serializer = self.serializer_class(instance=org_storage, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            org_id = self.kwargs.get('org_id')
            storage_id = self.kwargs.get('storage_id')
            org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
            org_storage.delete()
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)


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
        if queryset:
            serializer = self.get_serializer(queryset)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response({'detail': 'Организация не найдена.'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['storage'] = self.kwargs.get('id')
            serializer = self.get_serializer(data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Вид отхода не найден.'}, status=status.HTTP_404_NOT_FOUND)


class StorageWasteAPIView(APIView):
    serializer_class = StorageCapasitiesSerializer

    def get(self, request, *args, **kwargs):
        try:
            storage_id = self.kwargs.get('storage_id')
            waste_id = self.kwargs.get('waste_id')
            storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)
            serializer = self.serializer_class(storage_waste)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return Response({'detail': 'Неверный объект хранилища или вид отхода.'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, *args, **kwargs):
        try:
            storage_id = self.kwargs.get('storage_id')
            waste_id = self.kwargs.get('waste_id')
            storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)
            serializer = self.serializer_class(instance=storage_waste, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Неверный объект хранилища или вид отхода.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            storage_id = self.kwargs.get('storage_id')
            waste_id = self.kwargs.get('waste_id')
            storage_waste = get_object_or_404(StorageWasteTypeModel, storage=storage_id, waste_type=waste_id)
            storage_waste.delete()
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Неверный объект хранилища или вид отхода.'}, status=status.HTTP_404_NOT_FOUND)
    

#  <--------------- Generate --------------->
class OrgGenerateAPIView(APIView):
    serializer_class = OrgWasteValuesSerilaizer

    def post(self, request, *args, **kwargs):
        try:
            request.data['organization'] = self.kwargs.get('id')
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            waste_value, created = OrganizationWasteValuesModel.objects.get_or_create(organization=data['organization'], waste_type=data['waste_type'], defaults={'value': data['value']})
            if not created:
                waste_value.value += data['value']
                waste_value.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            org = self.kwargs.get('id')
            instance = get_object_or_404(OrganizationWasteValuesModel, organization=org, waste_type=request.data['waste_type'])
            serializer = self.serializer_class(instance=instance, data={'value': request.data['value']}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({'detail': 'Неверный объект организации или вид отхода.'}, status=status.HTTP_404_NOT_FOUND)


#  <--------------- Send --------------->
class OrgSendAPIView(APIView):
    def post(self, request, *args, **kwargs):
        organization = self.kwargs.get('id')
        wastes = OrganizationWasteValuesModel.objects.select_related('waste_type').filter(organization=organization)
        waste_values = dict()

        for waste in wastes:
            if waste.value != 0:
                waste_values[waste.waste_type.id] = waste.value

        if not waste_values.values():
            return Response({'detail': 'Нет отходов для переработки.'}, status=status.HTTP_400_BAD_REQUEST)
        
        organization_storages = OrganizationStorageModel.objects.select_related('storage', 'organization').order_by('interval').filter(organization=organization)

        if not organization_storages.values():
            return Response({'detail': 'У данной организации нет хранилищей для перерпботки.'}, status=status.HTTP_400_BAD_REQUEST)

        old_waste_values = waste_values.copy()
        waste_set = set()
        distance = {}

        for storage in organization_storages:
            storage_wastes = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=storage.storage)
            if sum(waste_values.values()) != 0:
                for waste in storage_wastes:
                    waste_set.add(waste.waste_type.id)
                    waste_capacity = waste.max_capacity - waste.current_capacity
                    if waste.waste_type.id in waste_values.keys() and waste_capacity != 0:
                        distance.setdefault(storage.id, storage.interval)
                        need_eat = waste_values[waste.waste_type.id]
                        if need_eat > 0:
                            ate = need_eat - waste_capacity
                            if ate <= 0:
                                waste_values[waste.waste_type.id] = 0
                                value = 0
                                waste.current_capacity += need_eat
                                waste.save()
                            else:
                                value = abs(ate)
                                waste.current_capacity = waste.max_capacity
                                waste.save()
                            waste_values[waste.waste_type.id] = value
                            org_value = OrganizationWasteValuesModel.objects.get(organization=organization, waste_type=waste.waste_type)
                            org_value.value = value
                            org_value.save()

        responce_dict = {
            'storage_responses': {},
            'total_distance': sum(distance.values())
        }

        for key, value in old_waste_values.items():
            if waste_values[key] != value:
                if waste_values[key] == 0:
                    responce_dict['storage_responses'][key] = 'completely'
                else:
                    responce_dict['storage_responses'][key] = 'partially'
            else:
                if waste_values[key] != 0 and key not in waste_set:
                    responce_dict['storage_responses'][key] = 'no_storage'
                else:
                    responce_dict['storage_responses'][key] = 'crowded'

        return Response(responce_dict, status=status.HTTP_207_MULTI_STATUS)
