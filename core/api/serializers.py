from rest_framework import serializers

from api.models import WasteTypeModel, StorageModel, StorageWasteTypeModel


class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteTypeModel
        fields = ['name']


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageModel
        fields = ['name']


class StorageWasteTypeSerializer(serializers.ModelSerializer):
    waste_type = WasteTypeSerializer()

    class Meta:
        model = StorageWasteTypeModel
        fields = ['waste_type', 'capacity']


class StorageSerializer(serializers.ModelSerializer):
    waste_type = serializers.SerializerMethodField()
    
    class Meta:
        model = StorageModel
        fields = ['id', 'name', 'waste_type']

    def get_waste_type(self, obj):
        waste_type = StorageWasteTypeModel.objects.filter(storage=obj)
        return StorageWasteTypeSerializer(waste_type, many=True).data