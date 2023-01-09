from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from .models import Property, Advertisement, Reservation
from .serializers import PropertySerializer, AdvertisementSerializer, ReservationSerializer

"""
This file currently provides ModelViewSets for the following models:
- Property, represting real estate properties
- Advertisement, representing advertisements associated with real estate properties
- Reservation, representing reservation associated with an advertisement
"""

class PropertiesViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    # Restrict non-authenticated users.
    permission_classes = [permissions.IsAuthenticated]

    # Per specification, properties have no particular restrictions when being created, deleted or edited.
    http_method_names = ['get', 'post', 'put', 'delete', 'head']

    # Allow searching by currently available fields.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
            'code',
            'guest_vacancies',
            'bathrooms',
            'pets_allowed',
            'cleaning_cost',
            'activation_date',
            'creation_date',
            'update_date'
        ]

class AdvertisementsViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    # Restrict non-authenticated users.
    permission_classes = [permissions.IsAuthenticated]

    # Per specification, advertisements should not be deletable. 
    http_method_names = ['get', 'post', 'put', 'head']

    # Allow searching by currently available fields.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
            'property',
            'platform',
            'platform_tax',
            'creation_date',
            'update_date'
        ]

class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    # Restrict non-authenticated users.
    permission_classes = [permissions.IsAuthenticated]

    # Per specification, reservations should not be editable.
    http_method_names = ['get', 'post', 'delete', 'head']

    # Allow searching by currently available fields.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
            'code',
            'advertisement',
            'checkin_date',
            'checkout_date',
            'total_cost',
            'comment',
            'guests',
            'creation_date',
            'update_date'
        ]
