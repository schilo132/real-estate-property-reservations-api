from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
import random

"""
This file currently provides ModelViewSets for the following models:
- RealEstateProperty
- PropertyAdvertisement
- PropertyReservation
"""

# Function to generate a unique random code for each reservation
def random_unique_code():
    not_unique = True
    while not_unique:
        unique_code = random.randint(1, 99999)

        # Check the randomly generated code against the existing codes to see if its unique
        if not Reservation.objects.filter(code=unique_code):
            not_unique = False
    return unique_code

class Property(models.Model):

    # Fields per specification: Property code;
    code = models.IntegerField(
        null=False,
        blank=False,
        unique=True,
        validators=[MinValueValidator(1)])

    # Guest limit;
    guest_vacancies = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        validators=[MinValueValidator(1)])

    # Number of bathrooms;
    bathrooms = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        validators=[MinValueValidator(1)])

    # Wheter pets are allowed or not;
    pets_allowed = models.BooleanField(default=False)

    # Cleaning cost;
    cleaning_cost = models.DecimalField(
        null=False,
        blank=False,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])

    # Activation date;
    activation_date = models.DateField(auto_now_add=True)

    # Creation date and time;
    creation_date = models.DateTimeField(auto_now_add=True)

    # Update date and time.
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Property " + str(self.id)

class Advertisement(models.Model):

    # Per specification, a property may have multiple advertisements, but an advertisement may only refer to one property.
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE)

    # Further fields per specification: Advertisement hosting platform;
    platform = models.CharField(
        max_length=50,
        null=False,
        blank=False)

    # Platform tax;
    platform_tax = models.DecimalField(
        null=False,
        blank=False,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])

    # Creation date and time (set automatically);
    creation_date = models.DateTimeField(auto_now_add=True)

    # Update date and time (set automatically).
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Advertisement " + str(self.id)

class Reservation(models.Model):

    # Per specification, an announcement may have multiple reservations, but a reservation may only refer to one advertisement.
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE)

    # Further fields per specification: Reservation code (randomly generated, see random_unique_code() above);
    code = models.IntegerField(
        unique=True,
        default=random_unique_code,
        validators=[MinValueValidator(1)])

    # Check-in date;
    checkin_date = models.DateField()

    # Check-out date;
    checkout_date = models.DateField()

    # Total cost;
    total_cost = models.DecimalField(
        null=False,
        blank=False,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])

    # Comment field;
    comment = models.CharField(
        max_length=1000,
        null=False,
        blank=False)

    # Number of guests
    guests = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        validators=[MinValueValidator(1)])

    # Creation date and time (set automatically);
    creation_date = models.DateTimeField(auto_now_add=True)

    # Update date and time (set automatically).
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Reservation " + str(self.id)

    def clean(self):

        # Validate that the check-out date is always later than the check-in date.
        if self.checkin_date > self.checkout_date:
            raise ValidationError({'checkin_date':'Check-out date must be later than check-in date.'})

        # Validate that there's enough vacancies for the reservation to be valid on its own.
        if self.advertisement.property.guest_vacancies < self.guests:
            raise ValidationError({'guests':'Insufficient vacancies for reservation.'})

        # Validate that there's enough vacancies for the reservation to be valid alongside other reservations.
        occupied_checkin = 0
        occupied_checkout = 0
        for i in Reservation.objects.all():

            # Iterate through all reservations that are for the same property.
            if self.advertisement.property == i.advertisement.property:

                # Check for vacancy conflicts when the check-in date is within another reservation's time frame.
                if (self.checkin_date >= i.checkin_date and self.checkin_date <= i.checkout_date):
                    
                    # Add up all the guests that are already supposed to be checked-in during the time frame.
                    occupied_checkin += i.guests

                    # If there's not enough remaining vacancies for the current reservation, raise an error.
                    if occupied_checkin + self.guests > self.advertisement.property.guest_vacancies:
                        raise ValidationError({'checkin_date':'Insufficient vacancies for reservation.'})

                # Check for vacancy conflicts when the check-out date is within another reservation's time frame.
                if (self.checkout_date >= i.checkin_date and self.checkout_date <= i.checkout_date):

                    # Add up all the guests that are already supposed to be checked-in during the time frame.
                    occupied_checkout += i.guests

                    # If there's not enough remaining vacancies for the current reservation, raise an error.
                    if occupied_checkout + self.guests > self.advertisement.property.guest_vacancies:
                        raise ValidationError({'checkout_date':'Insufficient vacancies for reservation.'})

    # Override save() method to make sure clean() is called.
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
