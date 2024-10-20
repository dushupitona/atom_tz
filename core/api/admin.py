from django.contrib import admin

from api.models import WasteTypeModel, OrganizationModel, StorageModel, \
      StorageWasteTypeModel, OrganizationStorageModel, \
      OrganizationWasteValuesModel


class OrgAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'name')


class WasteTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'name')


class StorageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'name')


class StorageWasteAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'storage', 'waste_type', 'max_capacity', 'current_capacity')


class OrgWasteValuesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'organization', 'waste_type', 'value')


class OrgStorageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'organization', 'storage', 'interval')



admin.site.register(WasteTypeModel, WasteTypeAdmin)
admin.site.register(OrganizationModel, OrgAdmin)
admin.site.register(StorageModel, StorageAdmin)
admin.site.register(StorageWasteTypeModel, StorageWasteAdmin)
admin.site.register(OrganizationStorageModel, OrgStorageAdmin)
admin.site.register(OrganizationWasteValuesModel, OrgWasteValuesAdmin)