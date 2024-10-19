from rest_framework import serializers

from api.models import WasteTypeModel, StorageModel, StorageWasteTypeModel, OrganizationModel,\
    OrganizationStorageModel

#  <--------------- Waste --------------->
class WasteTypeIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypeModel
        fields = ['id']


class WasteTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypeModel
        fields = ['name']


#  <--------------- Storage --------------->
class StorageIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModel
        fields = ['id']


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
class OrgIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = ['id']


class OrgNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationModel
        fields = ['name']


#  <--------------- Org Storage --------------->
class OrgStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStorageModel
        fields = ['organization', 'storage', 'interval']


class OrgStorageIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationStorageModel
        fields = ['interval']


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