from rest_framework import serializers
from .models import Property, Advertisement, Reservation

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id',
            'code',
            'guest_vacancies',
            'bathrooms',
            'pets_allowed',
            'cleaning_cost',
            'activation_date',
            'creation_date',
            'update_date'
        ]

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'id',
            'property',
            'platform',
            'platform_tax',
            'creation_date',
            'update_date'
        ]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
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
