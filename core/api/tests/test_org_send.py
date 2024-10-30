from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import OrganizationModel, WasteTypeModel, OrganizationWasteValuesModel, StorageModel, StorageWasteTypeModel,\
    OrganizationStorageModel

class OrgSendAPITestCase(APITestCase):
    def setUp(self):
        self.org1 = OrganizationModel.objects.create(name='org1')

        self.storage1 = StorageModel.objects.create(name='org1')
        self.storage2 = StorageModel.objects.create(name='org2')
        self.storage3= StorageModel.objects.create(name='org3')

        OrganizationStorageModel.objects.create(organization=self.org1, storage=self.storage1, interval=2000)
        self.org_s2 = OrganizationStorageModel.objects.create(organization=self.org1, storage=self.storage2, interval=1500)
        self.org_s3 = OrganizationStorageModel.objects.create(organization=self.org1, storage=self.storage3, interval=2300)

        self.waste1 = WasteTypeModel.objects.create(name='bio')
        self.waste2 = WasteTypeModel.objects.create(name='glass')
        self.waste3 = WasteTypeModel.objects.create(name='plastic')

        # storage 1
        self.s1_w1 = StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste1, max_capacity=1000)
        self.s1_w2 = StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste2, max_capacity=500)
        self.s1_w3 = StorageWasteTypeModel.objects.create(storage=self.storage1, waste_type=self.waste3, max_capacity=765)
        # storage 2
        self.s2_w1 = StorageWasteTypeModel.objects.create(storage=self.storage2, waste_type=self.waste1, max_capacity=1000)
        self.s2_w2 = StorageWasteTypeModel.objects.create(storage=self.storage2, waste_type=self.waste2, max_capacity=300)
        # storage 3
        self.s3_w3 = StorageWasteTypeModel.objects.create(storage=self.storage3, waste_type=self.waste3, max_capacity=1000)

        self.org_waste1 = OrganizationWasteValuesModel.objects.create(organization=self.org1, waste_type=self.waste1, value=1750)
        self.org_waste2 = OrganizationWasteValuesModel.objects.create(organization=self.org1, waste_type=self.waste2, value=200)
        self.org_waste3 = OrganizationWasteValuesModel.objects.create(organization=self.org1, waste_type=self.waste3, value=1000)

    def test_send(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})

        responce = self.client.post(url)

        # storage 1
        self.s1_w1.refresh_from_db()
        self.s1_w2.refresh_from_db()
        self.s1_w3.refresh_from_db()
        # storage 2
        self.s2_w1.refresh_from_db()
        self.s2_w2.refresh_from_db()
        # storage 3
        self.s3_w3.refresh_from_db()

        self.assertEqual(status.HTTP_207_MULTI_STATUS, responce.status_code)
        # waste 1
        self.assertEqual(self.s2_w1.current_capacity, self.s2_w1.max_capacity)
        self.assertEqual(self.s1_w1.current_capacity, 750)
        # waste 2
        self.assertEqual(self.s2_w2.current_capacity, 200)
        # waste 3
        self.assertEqual(self.s1_w3.current_capacity, self.s1_w3.max_capacity)
        self.assertEqual(self.s3_w3.current_capacity, 235)

    def test_send_crowded_after(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.org_waste3.value = 3000
        self.org_waste3.save()

        responce = self.client.post(url)

        # storage 3
        self.s3_w3.refresh_from_db()
        self.s1_w3.refresh_from_db()
        self.org_waste3.refresh_from_db()

        self.assertEqual(status.HTTP_207_MULTI_STATUS, responce.status_code)
    
        # waste 3
        self.assertEqual(self.s1_w3.current_capacity, self.s1_w3.max_capacity)
        self.assertEqual(self.s3_w3.current_capacity, self.s3_w3.max_capacity)
        self.assertEqual(self.org_waste3.value, 1235)

    def test_send_crowded_before(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.s1_w2.current_capacity =  self.s1_w2.max_capacity
        self.s2_w2.current_capacity =  self.s2_w2.max_capacity
        self.s1_w2.save()
        self.s2_w2.save()

        self.s1_w2.refresh_from_db()
        self.s2_w2.refresh_from_db()

        responce = self.client.post(url)

        self.assertEqual(status.HTTP_207_MULTI_STATUS, responce.status_code)
        self.assertEqual(responce.data['storage_responses'][self.waste1.id], 'completely')
        self.assertEqual(responce.data['storage_responses'][self.waste2.id], 'crowded')
        self.assertEqual(responce.data['storage_responses'][self.waste3.id], 'completely')

    def test_send_responce_check1(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.storage1.delete()

        responce = self.client.post(url)

        self.assertEqual(status.HTTP_207_MULTI_STATUS, responce.status_code)
        self.assertEqual(responce.data['total_distance'], self.org_s2.interval + self.org_s3.interval)
        self.assertEqual(responce.data['storage_responses'][self.waste1.id], 'partially')
        self.assertEqual(responce.data['storage_responses'][self.waste2.id], 'completely')
        self.assertEqual(responce.data['storage_responses'][self.waste3.id], 'completely')


    def test_send_responce_check2(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.storage1.delete()
        self.storage2.delete()

        responce = self.client.post(url)

        self.assertEqual(status.HTTP_207_MULTI_STATUS, responce.status_code)
        self.assertEqual(responce.data['total_distance'], self.org_s3.interval)
        self.assertEqual(responce.data['storage_responses'][self.waste1.id], 'no_storage')
        self.assertEqual(responce.data['storage_responses'][self.waste2.id], 'no_storage')
        self.assertEqual(responce.data['storage_responses'][self.waste3.id], 'completely')

    def test_send_bad_no_wastes(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.waste1.delete()
        self.waste2.delete()
        self.waste3.delete()

        responce = self.client.post(url)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

    def test_send_bad_no_storages(self):
        url = reverse_lazy('api:org_send', kwargs={'id': self.org1.id})
        self.storage1.delete()
        self.storage2.delete()
        self.storage3.delete()

        responce = self.client.post(url)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)
