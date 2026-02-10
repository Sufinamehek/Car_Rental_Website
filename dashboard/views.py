from django.shortcuts import render
from cars.models import Car
from bookings.models import Booking

def admin_dashboard(request):
    total_cars = Car.objects.count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='Pending').count()
    completed_bookings = Booking.objects.filter(status='Completed').count()

    bookings = Booking.objects.select_related('user', 'car').order_by('-created_at')

    context = {
        'total_cars': total_cars,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'bookings': bookings,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
