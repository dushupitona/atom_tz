from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy, reverse
from django.http import Http404

from api.models import OrganizationModel, WasteTypeModel, OrganizationWasteValuesModel


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

    def test_get_bad_id(self):
        url = reverse_lazy('api:org_object', kwargs={'id': 222})
        responce = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_update_org_object(self):
        url = reverse_lazy('api:org_object', kwargs={'id': self.org1.id})
        data = {
             'name': 'new_org_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, responce.status_code)
        self.org1.refresh_from_db()
        self.assertEqual(self.org1.name, data['name'])

    def test_update_bad_id(self):
        url = reverse_lazy('api:org_object', kwargs={'id': 222})
        data = {
             'name': 'new_org_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)

    def test_delete_org_object(self):
        url = reverse_lazy('api:org_object', kwargs={'id': self.org1.id})
        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(OrganizationModel.objects.filter(id=self.org1.id).exists())
    
    def test_delete_bad_id(self):
        url = reverse_lazy('api:org_object', kwargs={'id': 222})
        responce = self.client.delete(url, format='json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
    