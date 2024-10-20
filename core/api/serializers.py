from rest_framework import serializers
from rest_framework.exceptions import ValidationError 

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


class StorageCapasitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageWasteTypeModel
        fields = ['max_capacity', 'current_capacity']


#  <--------------- Organization Waste Value--------------->
class OrgWasteValuesSerilaizer(serializers.ModelSerializer):
    waste = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationWasteValuesModel
        fields = ['organization', 'waste_type', 'value']


