from rest_framework import serializers

from api.models import WasteTypeModel, StorageModel, StorageWasteTypeModel, OrganizationModel,\
    OrganizationStorageModel, OrganizationWasteValuesModel

#  <--------------- Waste --------------->
class WasteTypeListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
            return [obj.id for obj in instance]

class WasteTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypeModel
        fields = ['name']


#  <--------------- Storage --------------->
class StorageListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
            return [obj.id for obj in instance]


class StorageNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModel
        fields = ['name']


# class StorageWasteTypeSerializer(serializers.ModelSerializer):
#     waste_type = WasteTypeSerializer()

#     class Meta:
#         model = StorageWasteTypeModel
#         fields = ['waste_type', 'capacity']


# class StorageSerializer(serializers.ModelSerializer):
#     waste_type = serializers.SerializerMethodField()
    
#     class Meta:
#         model = StorageModel
#         fields = ['id', 'name', 'waste_type']

#     def get_waste_type(self, obj):
#         waste_type = StorageWasteTypeModel.objects.filter(storage=obj)
#         return StorageWasteTypeSerializer(waste_type, many=True).data
    

#  <--------------- Organization --------------->
class OrgListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
            return [obj.id for obj in instance]
    

class OrgCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationModel
        fields = ['name']


class OrgRetrieveSerializer(serializers.ModelSerializer):
    waste = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationModel
        fields = ['name', 'waste']

    def get_waste(self, obj):
        org_wastes = OrganizationWasteValuesModel.objects.select_related('waste_type').filter(organization=obj.id)
        return {waste.waste_type.id: waste.value for waste in org_wastes}


#  <--------------- Org Storage --------------->
class OrgStorageListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
            return [obj.storage.id for obj in instance]
    

class OrgStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStorageModel
        fields = ['organization', 'storage', 'interval']


class OrgStorageIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStorageModel
        fields = ['interval']



#  <--------------- Storage Waste --------------->
class StorageWasteListSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
            return [obj.waste_type.id for obj in instance]
    

class StorageWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageWasteTypeModel
        fields = ['storage', 'waste_type', 'max_capacity']





























# class OrganizationIDSerializer(serializers.Serializer):
#     organization = serializers.IntegerField()

#     def validate_organization(self, value):
#         org = OrganizationModel.objects.filter(id=value)
#         if org.exists():
#             return org
#         raise serializers.ValidationError('Invalid organization id.')


# class WasteValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ...
#         fields = ['value']


# class GenerateWasteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ...
#         fields = ['waste_type', 'value']
        

# class WasteOperationSerializer(serializers.Serializer):
#     organization = serializers.IntegerField()
#     wastes = GenerateWasteSerializer(many=True)

#     def validate_organization(self, value):
#         org = OrganizationModel.objects.filter(id=value)
#         if org.exists():
#             return org
#         raise serializers.ValidationError('Invalid organization id.')