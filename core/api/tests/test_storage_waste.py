from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import WasteTypeModel, StorageModel, StorageWasteTypeModel


#  <--------------- Storage & Waste  --------------->
class StorageWasteAPITestCase(APITestCase):
    def setUp(self):
        self.storage1 = StorageModel.objects.create(name='test_storage_1')
        self.waste1 = WasteTypeModel.objects.create(name='test_waste_1')
        self.waste2 = WasteTypeModel.objects.create(name='test_waste_2')
        self.waste3 = WasteTypeModel.objects.create(name='test_waste_3')
        self.storage_waste1 = StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste1, max_capacity=1000)
        StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste2, max_capacity=1530)

    def test_get(self):
        url = reverse_lazy('api:storage_waste', kwargs={'id': self.storage1.id})
        responce = self.client.get(url)
        expected_data = list(StorageWasteTypeModel.objects.select_related('waste_type').filter(storage=self.storage1).values_list('waste_type__id', flat=True))

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_post(self):
        url = reverse_lazy('api:storage_waste', kwargs={'id': self.storage1.id})
        data = {
             'waste_type': self.waste3.id,
             'max_capacity': 6700,
        }

        expected_count = StorageWasteTypeModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, StorageWasteTypeModel.objects.count())

#  <--------------- Storage & Waste object --------------->
    def test_get_object(self):
        url = reverse_lazy('api:storage_waste_object', kwargs={
             'storage_id': self.storage1.id,
             'waste_id': self.waste1.id
        })

        responce = self.client.get(url)
        storage_waste = StorageWasteTypeModel.objects.get(storage=self.storage1, waste_type=self.waste1)
        expected_data = {
             'max_capacity': storage_waste.max_capacity,
             'current_capacity': storage_waste.current_capacity
        }

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_put_object(self):
        url = reverse_lazy('api:storage_waste_object', kwargs={
             'storage_id': self.storage1.id,
             'waste_id': self.waste1.id
        })

        data = {
             'max_capacity': 8796,
             'current_capacity': 5347
        }

        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.storage_waste1.refresh_from_db()
        self.assertEqual(self.storage_waste1.max_capacity, data['max_capacity'])
        self.assertEqual(self.storage_waste1.current_capacity, data['current_capacity'])

    def test_delete_object(self):
        url = reverse_lazy('api:storage_waste_object', kwargs={
             'storage_id': self.storage1.id,
             'waste_id': self.waste1.id
        })

        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(StorageWasteTypeModel.objects.filter(storage=self.storage1.id, waste_type=self.waste1.id).exists())

