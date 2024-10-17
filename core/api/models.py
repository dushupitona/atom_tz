from django.db import models


class WasteTypeModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class OrganizationModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'
    

class StorageModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'
    

class OrganizationGenerateWasteModel(models.Model):
    organization = models.ForeignKey(to=OrganizationModel, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(to=WasteTypeModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.organization} | {self.waste_type} | {self.value}'


class OrganizationSendWasteModel(models.Model):
    organization = models.ForeignKey(to=OrganizationModel, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(to=WasteTypeModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.organization} | {self.waste_type} | {self.value}'


class StorageWasteTypeModel(models.Model):
    storage = models.ForeignKey(to=StorageModel, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(to=WasteTypeModel, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.storage} | {self.waste_type} | {self.capacity}'


class OrganizationStorage(models.Model):
    organization = models.ForeignKey(to=OrganizationModel, on_delete=models.CASCADE)
    storage = models.ForeignKey(to=StorageModel, on_delete=models.CASCADE)
    interval = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.organization} | {self.storage} | {self.interval}'



