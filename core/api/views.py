from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView,\
    RetrieveDestroyAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status

from api.models import OrganizationWasteValuesModel, OrganizationModel, StorageModel, StorageWasteTypeModel,\
    WasteTypeModel, OrganizationStorageModel

from api.serializers import OrgListSerializer, OrgRetrieveSerializer, StorageNameSerializer, StorageListSerializer,\
    WasteTypeListSerializer, WasteTypeNameSerializer, OrgStorageSerializer, OrgStorageIntervalSerializer, \
    StorageWasteSerializer, OrgCreateUpdateSerializer


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
    serializer_class = OrgStorageSerializer

    def get(self, request, *args, **kwargs):
        org_storages = OrganizationStorageModel.objects.select_related('storage').filter(organization=self.kwargs.get('id'))
        storage_list = [storage.storage.id for storage in org_storages]
        return Response(status=status.HTTP_200_OK, data=storage_list)
    
    def post(self, request, *args, **kwargs):
        request.data['organization'] = self.kwargs.get('id')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response()


class OrgStorageAPIView(APIView):
    serializer_class = OrgStorageIntervalSerializer

    def get(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
        serializer = self.serializer_class(instance=org_storage)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)

        serializer = self.serializer_class(instance=org_storage, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response()
    
    def delete(self, request, *args, **kwargs):
        org_id = self.kwargs.get('org_id')
        storage_id = self.kwargs.get('storage_id')
        org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
        org_storage.delete()
        return Response()


#  <--------------- Storage & Waste --------------->
class StorageWasteListAPIView(GenericAPIView):
    queryset = OrganizationStorageModel.objects.all()
    serializer_class = StorageWasteSerializer

    def get(self, request, *args, **kwargs):
        storage_wastes = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=self.kwargs.get('id'))
        waste_list = [waste.waste_type.id for waste in storage_wastes]
        return Response(status=status.HTTP_200_OK, data=waste_list)
    
    def post(self, request, *args, **kwargs):
        request.data['storage'] = self.kwargs.get('id')
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)


# class OrgStorageAPIView(APIView):
#     serializer_class = OrgStorageIntervalSerializer

#     def get(self, request, *args, **kwargs):
#         org_id = self.kwargs.get('org_id')
#         storage_id = self.kwargs.get('storage_id')
#         org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
#         serializer = self.serializer_class(instance=org_storage)
#         return Response(serializer.data)
    
#     def put(self, request, *args, **kwargs):
#         org_id = self.kwargs.get('org_id')
#         storage_id = self.kwargs.get('storage_id')
#         org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)

#         serializer = self.serializer_class(instance=org_storage, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response()
    
#     def delete(self, request, *args, **kwargs):
#         org_id = self.kwargs.get('org_id')
#         storage_id = self.kwargs.get('storage_id')
#         org_storage = get_object_or_404(OrganizationStorageModel, organization=org_id, storage=storage_id)
#         org_storage.delete()
#         return Response()
    



















# class StorageDetailAPIView(RetrieveAPIView):
#     queryset = StorageModel.objects.all()
#     serializer_class = StorageSerializer


# class StorageListAPIView(APIView):
#     def get(self, request):
#         my_objects = WasteTypeModel.objects.all()
#         ids = [obj.id for obj in my_objects]
#         return Response(ids)
    

# class GenerateWasteAPIView(APIView):
#     def post(self, request):
#         # serializer = WasteOperationSerializer(data=request.data) # из заголовка брать id компании
#         # serializer.is_valid()
#         # print(serializer.errors) if serializer.errors else None
#         # valid_data = serializer.validated_data
#         # print(valid_data)

#         # for waste in valid_data['wastes']:
#         #     OrganizationGenerateWasteModel.objects.create(
#         #         organization=valid_data['organization'].first(),
#         #         waste_type=waste['waste_type'],
#         #         value=waste['value']
#         #     )

#         return Response(status=201)
    

# class SendWasteAPIView(APIView):
#         def post(self, request):
#             serializer = WasteOperationSerializer(data=request.data) # из заголовка брать id компании
#             serializer.is_valid()
#             print(serializer.errors) if serializer.errors else None
#             valid_data = serializer.validated_data
            
#             org = valid_data['organization']
#             wastes = valid_data['wastes']
#             print('------------------ Serializers requests ------------------')

#             waste_values = {item['waste_type']: item['value'] for item in wastes}

#             print(waste_values)
            
#             organization_storages = OrganizationStorage.objects.select_related('storage', 'organization').order_by('interval').filter(organization=1)
            
#             for storage in organization_storages:
#                 storage_wastes = StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=storage.storage)
#                 for waste in storage_wastes:
#                     if waste.waste_type in waste_values.keys():
#                         need_eat = waste_values[waste.waste_type]
#                         if need_eat > 0:
#                             eat = need_eat - waste.capacity
#                             if eat < 0:
#                                 waste_values[waste.waste_type] = 0
#                             else:
#                                 waste_values[waste.waste_type] = eat

#             print(waste_values)
#             return Response(status=201)
        

    
# class TotalWasteOrganizationAPIView(APIView):
#     def get(self, request):
#         # serializer = OrganizationIDSerializer(data=self.request.data)
#         # if serializer.is_valid():
#         #     org = serializer.validated_data.get('organization')
#         #     queryset = OrganizationGenerateWasteModel.objects\
#         #         .values('waste_type').annotate(total=Sum('value')).order_by('waste_type').filter(organization=org.first())
#         #     return Response(queryset)
        
#         # print(serializer.errors)
#         return Response('Invalid id.')




#     # def post(self, request):
#     #     a = OrganizationGenerateWasteModel.objects.filter(organization=1).values('waste_type').annotate(total=Sum('value')).order_by('waste_type')
#     #     print(a)

#     #     return Response()