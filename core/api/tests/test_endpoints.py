from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import OrganizationModel, WasteTypeModel, StorageModel, OrganizationWasteValuesModel,\
    OrganizationStorageModel, StorageWasteTypeModel

#  <--------------- Organization --------------->
class OrgAPITestCase(APITestCase):
    def setUp(self):
            self.org1 = OrganizationModel.objects.create(name='test_org_1')
            OrganizationModel.objects.create(name='test_org_2')
            WasteTypeModel.objects.create(name='test_waste_1')
            WasteTypeModel.objects.create(name='test_waste_2')
            WasteTypeModel.objects.create(name='test_waste_3')
            [OrganizationWasteValuesModel.objects.create(organization=self.org1, waste_type=waste, value=1) for waste in WasteTypeModel.objects.all()]

    def test_create_org(self):
        url = reverse_lazy('api:org')
        data = {
            'name': 'test_org'
        }
        expected_count = OrganizationModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, OrganizationModel.objects.count())

    def test_org_list(self):
            url = reverse_lazy('api:org')
            responce = self.client.get(url)
            expected_data = list(OrganizationModel.objects.values_list('id', flat=True))
            
            self.assertEqual(status.HTTP_200_OK, responce.status_code)
            self.assertEqual(expected_data, responce.data)

#  <--------------- Org object --------------->
    def test_get_org_object(self):
        url = reverse_lazy('api:org_object', kwargs={'id': self.org1.id})
        responce = self.client.get(url)
        expected_data = {
             'name': self.org1.name,
             'waste': {}
        }

        for waste in OrganizationWasteValuesModel.objects.select_related('waste_type').all():
             expected_data['waste'][waste.id] = waste.value
        
        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_update_org_object(self):
        url = reverse_lazy('api:org_object', kwargs={'id': self.org1.id})
        data = {
             'name': 'new_org_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.org1.refresh_from_db()
        self.assertEqual(self.org1.name, data['name'])

    def test_delete_org_object(self):
        url = reverse_lazy('api:org_object', kwargs={'id': self.org1.id})
        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(OrganizationModel.objects.filter(id=self.org1.id).exists())
    

#  <--------------- Waste --------------->
class WasteAPITestCase(APITestCase):
    def setUp(self):
        self.waste1 = WasteTypeModel.objects.create(name='test_waste_1')
        WasteTypeModel.objects.create(name='test_waste_2')

    def test_create_waste_type(self):
        url = reverse_lazy('api:waste')
        data = {
            'name': 'test_waste_type'
        }
        expected_count = WasteTypeModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, WasteTypeModel.objects.count())

    def test_waste_list(self):
            url = reverse_lazy('api:waste')
            responce = self.client.get(url)
            expected_data = list(WasteTypeModel.objects.values_list('id', flat=True))
            
            self.assertEqual(status.HTTP_200_OK, responce.status_code)
            self.assertEqual(expected_data, responce.data)

#  <--------------- Waste object --------------->
    def test_get_waste_object(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': self.waste1.id})
        responce = self.client.get(url)
        expected_data = {'name': self.waste1.name}

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

    def test_update_waste_object(self):
        waste1 = WasteTypeModel.objects.create(name='test_waste_1')
        url = reverse_lazy('api:waste_object', kwargs={'id': waste1.id})
        data = {
             'name': 'new_waste_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        waste1.refresh_from_db()
        self.assertEqual(waste1.name, data['name'])

    def test_delete_waste_object(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': self.waste1.id})
        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(WasteTypeModel.objects.filter(id=self.waste1.id).exists())


#  <--------------- Storage --------------->
class StorageAPITestCase(APITestCase):
    def setUp(self):
        self.storage1 = StorageModel.objects.create(name='test_storage_1')
        StorageModel.objects.create(name='test_storage_2')

    def test_create_storage_type(self):
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

#  <--------------- Org & Storage object --------------->
    def test_get_object(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
             'org_id': self.org1.id,
             'storage_id': self.storage1.id
             }
        )

        responce = self.client.get(url)
        expected_data = {'interval': OrganizationStorageModel.objects.get(organization=self.org1, storage=self.storage1).interval}

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertEqual(expected_data, responce.data)

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

    def test_delete_object(self):
        url = reverse_lazy('api:org_storage_object', kwargs={
             'org_id': self.org1.id,
             'storage_id': self.storage1.id
        })

        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(OrganizationStorageModel.objects.filter(organization=self.org1.id, storage=self.storage1.id).exists())


#  <--------------- Storage & Waste  --------------->
class StorageWasteAPITestCase(APITestCase):
    def setUp(self):
        self.storage1 = StorageModel.objects.create(name='test_storage_1')
        self.waste1 = WasteTypeModel.objects.create(name='test_waste_1')
        self.waste2 = WasteTypeModel.objects.create(name='test_waste_2')
        self.waste3 = WasteTypeModel.objects.create(name='test_waste_3')
        StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste1, max_capacity=1000)
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

