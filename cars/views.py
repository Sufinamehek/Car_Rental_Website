# # from django.shortcuts import render
# # from .models import Car

# # def car_list(request):
# #     cars = Car.objects.all()  # Get all cars from database
# #     return render(request, 'cars/car_list.html', {'cars': cars})

# # # from django.shortcuts import render

# # # def car_list(request):
# # #     # Dummy list of cars (temporary, no database needed)
# # #     cars = [
# # #         {"name": "Toyota Corolla", "price_per_day": 50, "price_per_km": 1.5, "is_available": True},
# # #         {"name": "Honda Civic", "price_per_day": 60, "price_per_km": 1.8, "is_available": False},
# # #         {"name": "Suzuki Swift", "price_per_day": 40, "price_per_km": 1.2, "is_available": True},
# # #     ]
# # # #     return render(request, 'cars/car_list.html', {'cars': cars})
# # # def book_car(request, id):
# # #     car = Car.objects.get(id=id)
# # #     return render(request, 'cars/book_car.html', {'car': car})
# from django.shortcuts import render
# from .models import Car

# def car_list(request):
#     cars = Car.objects.all()
#     return render(request, 'cars/car_list.html', {'cars': cars})


# from pyexpat.errors import messages
from django.shortcuts import render
from .models import Car
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Car
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Car, Booking
from django.utils import timezone

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'accounts/signup.html')

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Check if user is owner or admin
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, "You cannot cancel this booking.")
        return redirect('cars:user_bookings')  # user booking list

    # Check 24 hours limit
    if booking.can_cancel():
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "Booking cannot be cancelled after 24 hours.")

    # Redirect based on role
    if request.user.is_staff:
        return redirect('/admin/cars/booking/')  # admin booking list
    else:
        return redirect('cars:user_bookings')  # user booking list

# views.py
from .models import Car

def home(request):
    cars = Car.objects.all()[:6]   # sirf 6 cars
    print("Cars count:", cars.count())
    return render(request, 'home.html', {'cars': cars})

