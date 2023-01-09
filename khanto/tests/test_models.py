from os.path import join
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from khanto.views import PropertiesViewSet, AdvertisementsViewSet, ReservationsViewSet
from khanto.models import Property, Advertisement, Reservation
from http import HTTPStatus
from os.path import join
from rest_framework.test import force_authenticate, APIClient
import json

"""
This file currently tests for:
1 - Retrieving instances of the Property, Advertisement and Reservation models to
    confirm that the test fixtures were properly loaded and that the GET endpoints work
    (success expected);
2 - Deleting a Advertisement model instance (error expected);
3 - Editing a Reservation model instance (error expected);
4 - Creating a Reservation model instance where the check-in date is later than the
    check-out date (error expected);
5 - Creating a Reservation model instance where the check-in date falls within the
    time frame of at least one different reservation and the sum of their number of
    guests exceeds the number of vacancies for the corresponding property (error
    expected);
6 - Creating a Reservation model instance where the check-out date falls within the
    time frame of at least one different reservation and the sum of their number of
    guests exceeds the number of vacancies for the corresponding property (error
    expected);
"""

class ModelViewSetTest(TestCase):

    # Load the model data from the fixtures in the "khanto/fixtures" path
    test_fixtures = [
        'test_properties',
        'test_advertisements',
        'test_reservations',
    ]
    test_fixtures_list = []
    path_to_fixtures = join(str(settings.BASE_DIR), 'khanto/fixtures/')
    for test_fixture in test_fixtures:
        test_fixtures_list.append(path_to_fixtures + '{}.json'.format(test_fixture))
    fixtures = test_fixtures_list
    
    # Setup user authentication for permissions
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@test.com'
        )

    # Get a Property model instance
    def test_property_get(self):
        request = self.factory.get('/properties/')
        force_authenticate(request, user=self.user)
        response = PropertiesViewSet.as_view({'get': 'retrieve'})(request, pk = 1)

        # Confirm that the right instance was retrieved
        self.assertEqual(response.data, {'id': 1, 'code': 1, 'guest_vacancies': 3,
            'bathrooms': 2, 'pets_allowed': True, 'cleaning_cost': '10.00',
            'activation_date': '2023-01-05', 'creation_date': '2023-01-05T20:31:12.460000Z',
            'update_date': '2023-01-05T20:31:12.460000Z'})

        # Confirm that request was successful:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)

    # Get a Advertisement model instance
    def test_advertisement_get(self):
        request = self.factory.get('/advertisements/')
        force_authenticate(request, user=self.user)
        response = AdvertisementsViewSet.as_view({'get': 'retrieve'})(request, pk = 1)

        # Confirm that the right instance was retrieved
        self.assertEqual(response.data, {'id': 1, 'property': 1, 'platform': 'TestPlatform1',
            'platform_tax': '50.00', 'creation_date': '2023-01-05T20:33:36.345000Z',
            'update_date': '2023-01-05T20:33:36.345000Z'})

        # Confirm that request was successful:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)

    # Get a Reservation model instance
    def test_reservation_get(self):
        request = self.factory.get('/reservations/')
        force_authenticate(request, user=self.user)
        response = ReservationsViewSet.as_view({'get': 'retrieve'})(request, pk = 1)

        # Confirm that the right instance was retrieved
        self.assertEqual(response.data, {'id': 1, 'code': 36085, 'advertisement': 1,
            'checkin_date': '2023-01-06', 'checkout_date': '2023-01-07',
            'total_cost': '100.00', 'comment': 'Test1', 'guests': 2,
            'creation_date': '2023-01-06T19:08:55.580000Z',
            'update_date': '2023-01-06T19:08:55.580000Z'})

        # Confirm that request was successful:
        self.assertEqual(response.status_code, HTTPStatus.OK._value_)

    # Test if deleting fails for a Advertisement model instance
    def test_advertisement_delete(self):
        data = json.dumps({
            "property":1,
            "platform":"TestPlatform1",
            "platform_tax":"50.00",
            "creation_date":"2023-01-05T20:33:36.345Z",
            "update_date":"2023-01-05T20:33:36.345Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete('/advertisements/', data=data, content_type='application/json')
        
        # Confirm that the request failed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED._value_)


    # Test if editing fails for a Reservation model instance
    def test_reservation_edit(self):
        data = json.dumps({
            "code":36085,
            "advertisement":1,
            "checkin_date":"2023-01-06",
            "checkout_date":"2023-01-06",
            "total_cost":"100.00",
            "comment":"Test1Edited",
            "guests":2,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put('/reservations/', data=data, content_type='application/json')

        # Confirm that the request failed
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED._value_)

    # Test if check-in date later than check-out date fails for Reservation model
    def test_reservation_checkin_checkout(self):
        data = json.dumps({
            "code":36086,
            "advertisement":1,
            "checkin_date":"2023-01-07",
            "checkout_date":"2023-01-06",
            "total_cost":"100.00",
            "comment":"Test1Edited",
            "guests":2,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Confirm that there was an error during validation
        with self.assertRaises(ValidationError):
            response = client.post('/reservations/', data=data, content_type='application/json')

    # Test if check-in date later than check-out date fails for Reservation model
    def test_reservation_guest_limit_checkin(self):
        data = json.dumps({
            "code":36086,
            "advertisement":1,
            "checkin_date":"2023-01-07",
            "checkout_date":"2023-01-06",
            "total_cost":"100.00",
            "comment":"Test1Edited",
            "guests":2,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Confirm that there was an error during validation
        with self.assertRaises(ValidationError):
            response = client.post('/reservations/', data=data, content_type='application/json')

    # Test if number of guests in Reservation model instance higher than number of guest vacancies
    # for corresponding property fails.
    def test_reservation_guest_limit(self):
        data = json.dumps({
            "code":36087,
            "advertisement":1,
            "checkin_date":"2023-01-10",
            "checkout_date":"2023-01-11",
            "total_cost":"100.00",
            "comment":"Test1",
            "guests":20,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Confirm that there was an error during validation
        with self.assertRaises(ValidationError):
            response = client.post('/reservations/', data=data, content_type='application/json')


    # Test if number of guests in Reservation model instance is higher than number of guest vacancies
    # for corresponding property fails when the check-in date falls within the time frame of at
    # least one other reservation (for example, you try to make a reservation but all rooms are
    # occupied due to other reservations during the check-in date).
    def test_reservation_guest_limit_checkin(self):
        data = json.dumps({
            "code":36087,
            "advertisement":1,
            "checkin_date":"2023-01-06",
            "checkout_date":"2023-01-09",
            "total_cost":"100.00",
            "comment":"Test1",
            "guests":2,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Confirm that there was an error during validation
        with self.assertRaises(ValidationError):
            response = client.post('/reservations/', data=data, content_type='application/json')

    # Test if number of guests in Reservation model instance is higher than number of guest vacancies
    # for corresponding property fails when the check-out date falls within the time frame of at
    # least one other reservation (for example, you try to make a reservation but all rooms are
    # occupied due to other reservations during the check-out date).
    def test_reservation_guest_limit_checkout(self):
        data = json.dumps({
            "code":36087,
            "advertisement":1,
            "checkin_date":"2023-01-05",
            "checkout_date":"2023-01-07",
            "total_cost":"100.00",
            "comment":"Test1",
            "guests":2,
            "creation_date":"2023-01-06T19:08:55.580Z",
            "update_date":"2023-01-06T19:08:55.580Z"
        })
        client = APIClient()
        client.force_authenticate(user=self.user)

        # Confirm that there was an error during validation
        with self.assertRaises(ValidationError):
            response = client.post('/reservations/', data=data, content_type='application/json')
