from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import CheckConstraint

#  <--------------- Waste --------------->

class WasteTypeModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


#  <--------------- Storage ---------------> 

class StorageModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'
    

class StorageWasteTypeModel(models.Model):
    storage = models.ForeignKey(to=StorageModel, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(to=WasteTypeModel, on_delete=models.CASCADE)
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('storage', 'waste_type')
    
        constraints = [
            CheckConstraint(
                check=Q(current_capacity__lte=F('max_capacity')),
                name='check_capacity',
            ),
        ]

    def __str__(self):
        return f'{self.storage} | {self.waste_type} | {self.current_capacity}'


#  <--------------- Organization --------------->

class OrganizationModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class OrganizationStorageModel(models.Model):
    organization = models.ForeignKey(to=OrganizationModel, on_delete=models.CASCADE)
    storage = models.ForeignKey(to=StorageModel, on_delete=models.CASCADE)
    interval = models.PositiveIntegerField()

    class Meta:
        unique_together = ('organization', 'storage')


    def __str__(self):
        return f'{self.organization} | {self.storage} | {self.interval}'


class OrganizationWasteValuesModel(models.Model):
    organization = models.ForeignKey(to=OrganizationModel, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(to=WasteTypeModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.organization} | {self.waste_type} | {self.value}'



