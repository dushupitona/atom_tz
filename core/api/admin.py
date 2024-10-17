from django.contrib import admin

from api.models import WasteTypeModel, OrganizationModel, StorageModel, \
      OrganizationGenerateWasteModel, StorageWasteTypeModel, OrganizationStorage, \
      OrganizationSendWasteModel


admin.site.register(WasteTypeModel)
admin.site.register(OrganizationModel)
admin.site.register(StorageModel)
admin.site.register(OrganizationGenerateWasteModel)
admin.site.register(StorageWasteTypeModel)
admin.site.register(OrganizationStorage)
admin.site.register(OrganizationSendWasteModel)