from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from catalog.models import FlightsheetDetails, FlightsheetHeader
from api.serializers import FlightsheetDetailsSerializer, FlightsheetHeaderSerializer
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
import json
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# tests for views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_header(flight_date="", duty_instructor=""):
        if flight_date != "" and duty_instructor != "":
            FlightsheetHeader.objects.create(flight_date=flight_date, duty_instructor=duty_instructor)
    
    @staticmethod
    def create_detail(flight_key="", flight_date="", flight_number="", glider="", pilot1="", launch_time="", landing_time="", duration_time=""):
        if flight_key != "" and flight_date != "" and flight_number != "" and glider != "" and pilot1 != "" and launch_time != "" and landing_time != "" and duration_time != "":
            FlightsheetDetails.objects.create(flight_key=flight_key, flight_date=flight_date, flight_number=flight_number, glider=glider, pilot1=pilot1, launch_time=launch_time, landing_time=landing_time, duration_time=duration_time)

    def setUp(self):
        # add test data
        self.create_header("2021-12-01", "test_instructor")
        self.create_header("2021-12-02", "test_instructor")
        self.create_header("2021-12-03", "test_instructor")
        self.create_detail("2021-12-01-1", "2019-06-01", "1", "GYK", "test_pilot", "12:41:00", "12:56:00", "00:15:00")
        self.create_detail("2021-12-01-2", "2019-06-01", "2", "GYK", "test_pilot", "12:41:00", "12:56:00", "00:15:00")
        self.create_detail("2021-12-01-3", "2019-06-01", "3", "GYK", "test_pilot", "12:41:00", "12:56:00", "00:15:00")
        self.create_detail("2022-12-01-3", "2019-07-01", "3", "GYK", "test_pilot", "12:41:00", "12:56:00", "00:15:00")

class GetTest(BaseViewTest):

    def test_get_details(self):
        response = self.client.get(reverse("details_all"))
        # fetch the data from db
        expected = FlightsheetDetails.objects.all()
        serialized = FlightsheetDetailsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_many_details(self):
        response = self.client.delete('/api/detailsdate/2019-06-01/')
        expected = FlightsheetDetails.objects.filter(flight_date="2019-06-01")
        serialized = FlightsheetDetailsSerializer(expected, many=True)
#        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_add_detail(self):
        data_raw = {"flight_date":"2019-12-16","flight_number":"2","flight_key":"2019-12-16-2","glider":"GSP","pilot1":"Bob Hainsworth","pilot2":"","launch_time":"10:15:00","landing_time":"11:17:00","duration_time":"01:02:00","height":"28","billing_code":"MEM-P1","gfa_number":"","notes":"","tow_cost":"85.00","glider_cost":"62.00","cgc_cost":"0.00","pilot1_cost":"147.00","pilot2_cost":"0.00"}
#        data = JSONRenderer().render(data_raw)
        response = self.client.post('/api/details/', data_raw, content_type='application/json')
        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_header(self):
        response = self.client.post('/api/headers/', {'data': {"flight_date":"2019-12-16","duty_instructor":"Garrett Russell","instructor":"Barry McCarthy","air_experience_instructor":"Mark Morwood","duty_pilot":"David Farritor","tug_pilot1":"John Ashford","tug_pilot2":"Tug Pilot 2","runway":"06"}
            }, format='json')
        # fetch the data from db
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)