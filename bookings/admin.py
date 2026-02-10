

from django.contrib import admin
from .models import Car, Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'car',
        'start_date',
        'end_date',
        'status',
        'total_price',
        'can_cancel_admin',
    )

    def can_cancel_admin(self, obj):
        if obj.can_cancel:
            return "Yes"
        return "No"
    can_cancel_admin.short_description = "Can Cancel"

