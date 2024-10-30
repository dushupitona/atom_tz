from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import OrganizationModel, StorageModel, OrganizationStorageModel


#  <--------------- Org & Storage --------------->
class OrgStorageAPITestCase(APITestCase):
    def setUp(self):
        self.org1 = OrganizationModel.objects.create(name='test_org_1')
        self.storage1 = StorageModel.objects.create(name='test_storage_1')
        self.storage2 = StorageModel.objects.create(name='test_storage_2')
        self.storage3 = StorageModel.objects.create(name='test_storage_3')
        self.org_storage1 = OrganizationStorageModel.objects.create(organization=self.org1, storage=self.storage1, interval=1500)
        OrganizationStorageModel.objects.create(organization=self.org1, storage=self.storage2, interval=745)

    def test_get(self):
        url = reverse_lazy('api:org_storage', kwargs={'id': self.org1.id})
        responce = self.client.get(url)
        expected_data = list(OrganizationStorageModel.objects.select_related('storage').filter(organization=self.org1).values_list('storage__id', flat=True))

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_get_bad_id(self):
        url = reverse_lazy('api:org_storage', kwargs={'id': 222})
        responce = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_post(self):
        url = reverse_lazy('api:org_storage', kwargs={'id': self.org1.id})
        data = {
             'storage': self.storage3.id,
             'interval': self.org_storage1.interval
        }

        expected_count = OrganizationStorageModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, OrganizationStorageModel.objects.count())

    def test_post_bad_id(self):
        url = reverse_lazy('api:org_storage', kwargs={'id': 222})
        data = {
            'storage': self.storage3.id,
            'interval': 122
        }
        responce = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

    def test_post_bad_data(self):
        url = reverse_lazy('api:org_storage', kwargs={'id': self.org1.id})
        data = {
            'storage': 243,
            'interval': 122
        }
        responce = self.client.post(url, data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

#  <--------------- Org & Storage object --------------->
    def test_get_object(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
             'org_id': self.org1.id,
             'storage_id': self.storage1.id
        })

        responce = self.client.get(url)
        expected_data = {'interval': OrganizationStorageModel.objects.get(organization=self.org1, storage=self.storage1).interval}

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_get_bad_object_id(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': 222,
            'storage_id': self.storage3.id
        })
        responce = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': self.org1.id,
            'storage_id': 222
        })
        responce = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_put_object(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
             'org_id': self.org1.id,
             'storage_id': self.storage1.id
        })

        data = {
             'interval': 123456
        }

        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.org_storage1.refresh_from_db()
        self.assertEqual(self.org_storage1.interval, data['interval'])

    def test_put_bad_object_id(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': 222,
            'storage_id': self.storage3.id
        })
        responce = self.client.put(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': self.org1.id,
            'storage_id': 222
        })
        responce = self.client.put(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_put_bad_object_data(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
             'org_id': self.org1.id,
             'storage_id': self.storage1.id
        })

        data = {
             'interval': 'qwesda'
        }

        responce = self.client.put(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

    def test_delete_object(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': self.org1.id,
            'storage_id': self.storage1.id
        })

        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(OrganizationStorageModel.objects.filter(organization=self.org1.id, storage=self.storage1.id).exists())

    def test_delete_bad_object_id(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': 222,
            'storage_id': self.storage3.id
        })
        responce = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
        url = reverse_lazy('api:org_storage_object', kwargs={
            'org_id': self.org1.id,
            'storage_id': 222
        })
        responce = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)