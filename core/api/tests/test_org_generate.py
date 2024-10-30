from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import OrganizationModel, WasteTypeModel, OrganizationWasteValuesModel


class OrgGenerateAPITestCase(APITestCase):
    def setUp(self):
        self.org1 = OrganizationModel.objects.create(name='org1')
        self.waste1 = WasteTypeModel.objects.create(name='test_waste_1')
        self.waste2 = WasteTypeModel.objects.create(name='test_waste_2')
        self.org_waste =OrganizationWasteValuesModel.objects.create(organization=self.org1, waste_type=self.waste2, value=123)

    def test_generate_create(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': self.org1.id})
        data = {
             'waste_type': self.waste1.id,
             'value': 400
        }

        expected_count = OrganizationWasteValuesModel.objects.count() + 1
        responce = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.assertEqual(expected_count, OrganizationWasteValuesModel.objects.count())

    def test_generate_create_bad_id(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': 222})
        data = {
             'waste_type': self.waste1.id,
             'value': 400
        }

        responce = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

    def test_generate_create_bad_data(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': self.org1.id})
        data = {
             'waste_type': 4444,
             'value': 400
        }

        responce = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

        data = {
             'waste_type': self.waste1.id,
             'value': 'qweqew12'
        }

        responce = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

    def test_generate_update(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': self.org1.id})
        data = {
             'waste_type': self.waste2.id,
             'value': 10
        }

        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)

    def test_update_bad_id(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': 555})
        data = {
             'waste_type': self.waste2.id,
             'value': 10
        }

        responce = self.client.put(url, data, format='json')
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_generate_update_bad_data(self):
        url = reverse_lazy('api:org_generate', kwargs={'id': self.org1.id})
        data = {
             'waste_type': 4444,
             'value': 400
        }

        responce = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)

        data = {
             'waste_type': self.waste1.id,
             'value': 'qweqew12'
        }

        responce = self.client.post(url, data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, responce.status_code)