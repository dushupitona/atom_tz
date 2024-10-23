from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import OrganizationModel, StorageModel


#  <--------------- Storage --------------->
class StorageAPITestCase(APITestCase):
    def setUp(self):
        self.storage1 = StorageModel.objects.create(name='test_storage_1')
        StorageModel.objects.create(name='test_storage_2')

    def test_create_storage(self):
        url = reverse_lazy('api:storage')
        data = {
            'name': 'test_storage'
        }
        expected_count = StorageModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, StorageModel.objects.count())

    def test_storage_list(self):
            url = reverse_lazy('api:storage')
            responce = self.client.get(url)
            expected_data = list(StorageModel.objects.values_list('id', flat=True))

            self.assertEqual(status.HTTP_200_OK, responce.status_code)
            self.assertEqual(expected_data, responce.data)


#  <--------------- Storage object --------------->
    def test_get_storage_object(self):
        url = reverse_lazy('api:storage_object', kwargs={'id': self.storage1.id})
        responce = self.client.get(url)
        expected_data = {
             'name': self.storage1.name,
        }

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_update_storage_object(self):
        url = reverse_lazy('api:storage_object', kwargs={'id': self.storage1.id})
        data = {
             'name': 'new_storage_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.storage1.refresh_from_db()
        self.assertEqual(self.storage1.name, data['name'])

    def test_delete_waste_object(self):
        url = reverse_lazy('api:storage_object', kwargs={'id': self.storage1.id})
        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(OrganizationModel.objects.filter(id=self.storage1.id).exists())
