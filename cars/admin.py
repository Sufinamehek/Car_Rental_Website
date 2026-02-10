from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'car_type',
        'fare_per_km',
        'price_per_day',
        'seats',          # ✅ fixed here
        'is_available',
    )

    list_filter = ('car_type', 'is_available')
    search_fields = ('name',)
