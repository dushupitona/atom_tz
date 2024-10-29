from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse_lazy

from api.models import WasteTypeModel


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

    def test_get_bad_id(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': 222})
        responce = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
    
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

    def test_update_bad_id(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': 222})
        data = {
             'name': 'new_waste_name'
        }
        responce = self.client.put(url, data, format='json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)


    def test_delete_waste_object(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': self.waste1.id})
        responce = self.client.delete(url)

        self.assertEqual(status.HTTP_200_OK, responce.status_code)
        self.assertFalse(WasteTypeModel.objects.filter(id=self.waste1.id).exists())

    def test_delete_bad_id(self):
        url = reverse_lazy('api:waste_object', kwargs={'id': 222})
        responce = self.client.delete(url, format='json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, responce.status_code)
            