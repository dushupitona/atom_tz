from django.contrib import admin

from api.models import WasteTypeModel, OrganizationModel, StorageModel, \
      OrganizationWasteOperationModel, StorageWasteTypeModel, OrganizationStorageModel, \
      OrganizationWasteValuesModel


admin.site.register(WasteTypeModel)
admin.site.register(OrganizationModel)
admin.site.register(StorageModel)
admin.site.register(OrganizationWasteOperationModel)
admin.site.register(StorageWasteTypeModel)
admin.site.register(OrganizationStorageModel)
admin.site.register(OrganizationWasteValuesModel)