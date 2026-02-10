from django.db import models
from django.contrib.auth.models import User
from cars.models import Car
from django.utils import timezone
from datetime import timedelta

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),       # Booking made, not confirmed
        ('Confirmed', 'Confirmed'),   # Booking confirmed
        ('Ongoing', 'Ongoing'),       # Ride started
        ('Completed', 'Completed'),   # Ride ended
        ('Cancelled', 'Cancelled'),   # Booking cancelled
    ]

    PAYMENT_CHOICES = [
        ('Pending', 'Pending'),       # Not paid yet
        ('Paid', 'Paid'),             # Payment done
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)

    start_lat = models.FloatField(null=True, blank=True)
    start_lng = models.FloatField(null=True, blank=True)
    end_lat = models.FloatField(null=True, blank=True)
    end_lng = models.FloatField(null=True, blank=True)

    start_date = models.DateField()
    start_time = models.TimeField(default=timezone.now)

    end_date = models.DateField()
    end_time = models.TimeField(default=timezone.now)

    
    total_days = models.PositiveIntegerField(default=1) 
    total_km = models.FloatField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.car.name}"

    @property
    def start_datetime(self):
        """Combine start_date and start_time into a single datetime object"""
        from datetime import datetime
        return datetime.combine(self.start_date, self.start_time)

    @property
    def end_datetime(self):
        """Combine end_date and end_time into a single datetime object"""
        from datetime import datetime
        return datetime.combine(self.end_date, self.end_time)
    
    @property
    def can_cancel(self):
        """Booking can only be cancelled within 24 hours"""
        return timezone.now() - self.created_at <= timedelta(hours=24)
    
    @property
    def is_ongoing(self):
        """Check if ride is ongoing"""
        return self.status == 'Ongoing'
    
    @property
    def is_completed(self):
        return self.status == 'Completed'
    
    @property
    def is_paid(self):
        return self.payment_status == 'Paid'
