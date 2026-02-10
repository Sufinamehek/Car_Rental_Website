from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



class Car(models.Model):
    CAR_TYPE_CHOICES = [
        ('Economy', 'Economy'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Luxury', 'Luxury'),
        ('Electric', 'Electric'),
    ]

    name = models.CharField(max_length=100)
    car_type = models.CharField(
        max_length=50,
        choices=CAR_TYPE_CHOICES
    )
    fare_per_km = models.DecimalField(max_digits=6, decimal_places=2)
    price_per_day = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )
    seats = models.IntegerField(default=4)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='cars/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_bookings')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"

    def can_cancel(self):
        from django.utils import timezone
        from datetime import timedelta
        if self.status == 'Cancelled':
            return False
        now = timezone.now()
        return now <= self.created_at + timedelta(hours=24)
