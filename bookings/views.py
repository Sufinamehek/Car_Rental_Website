from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from math import ceil
from datetime import datetime, timedelta

from .models import Booking
from .forms import BookingForm
from cars.models import Car


from datetime import datetime
from decimal import Decimal
from math import ceil
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# @login_required(login_url='login')
def book_car(request, car_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to book a car.")
        return redirect("login")
    car = get_object_or_404(Car, id=car_id)

    # Initialize variables
    total_price = 0
    total_days = 0
    total_hours = 0
    allowed_km = 0
    service_charge = Decimal("500")
    insurance_charge = Decimal("300")

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            start_dt = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
            end_dt = datetime.combine(form.cleaned_data['end_date'], form.cleaned_data['end_time'])

            hours = (end_dt - start_dt).total_seconds() / 3600
            total_hours = round(hours, 1)
            total_days = max(1, ceil(hours / 24))
            allowed_km = total_days * 800
            total_price = (Decimal(total_days) * car.price_per_day) + service_charge + insurance_charge
            total_price = round(total_price, 2)

            # If user is just checking price → render page
            if "check_price" in request.POST:
                return render(request, "bookings/book_car.html", {
                    "form": form,
                    "car": car,
                    "total_price": total_price,
                    "total_days": total_days,
                    "total_hours": total_hours,
                    "allowed_km": allowed_km,
                    "service_charge": service_charge,
                    "insurance_charge": insurance_charge,
                })

            # If user confirms booking → create booking and redirect
            elif "confirm_booking" in request.POST:
                booking = form.save(commit=False)
                booking.car = car
                booking.user = request.user
                booking.total_days = total_days
                booking.total_price = total_price
                booking.start_time = start_dt
                booking.end_time = end_dt
                booking.status = "Pending"
                booking.payment_status = "Pending"
                booking.save()

                # Redirect to payment page safely
                return redirect("bookings:payment_method", booking_id=booking.id)

        # Form invalid → re-render with errors
        return render(request, "bookings/book_car.html", {
            "form": form,
            "car": car,
            "total_price": total_price,
            "total_days": total_days,
            "total_hours": total_hours,
            "allowed_km": allowed_km,
            "service_charge": service_charge,
            "insurance_charge": insurance_charge,
        })

    else:
        # GET request → show blank form
        form = BookingForm()

    return render(request, "bookings/book_car.html", {
        "form": form,
        "car": car,
        "total_price": total_price,
        "total_days": total_days,
        "total_hours": total_hours,
        "allowed_km": allowed_km,
        "service_charge": service_charge,
        "insurance_charge": insurance_charge,
    })

# BOOKING CONFIRM PAGE
@login_required
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "bookings/booking_confirm.html", {"booking": booking})



# USER BOOKINGS LIST
@login_required
def bookings_index(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/bookings_index.html', {'bookings': bookings})


# CANCEL BOOKING
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Permission check
    if request.user != booking.user and not request.user.is_staff:
        messages.error(request, "You are not allowed to cancel this booking.")
        return redirect('bookings:bookings_index')

    # 24 hour cancellation rule
    if timezone.now() - booking.created_at > timedelta(hours=24):
        messages.error(request, "Cancellation allowed only within 24 hours.")
        return redirect('bookings:bookings_index')

    booking.is_cancelled = True
    booking.save()

    messages.success(request, "Booking cancelled successfully.")
    return redirect('bookings:bookings_index')

@login_required

def payment_method(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        payment_option = request.POST.get("payment_option")
        if payment_option in ["COD", "Online"]:
            if payment_option == "Online":
                booking.payment_status = "Paid"
            booking.status = "Confirmed"
            booking.save()
            messages.success(request, f"Payment successful! Booking {booking.status}")
            return redirect("bookings:booking_confirm", booking_id=booking.id)
        else:
            messages.error(request, "Select a payment method!")
          

    return render(request, "bookings/payment_method.html", {"booking": booking})

# SUCCESS PAGE
@login_required
def booking_success(request):
    return render(request, 'bookings/booking_success.html')
@login_required
def ride_start(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.user or request.user.is_staff:
        booking.status = "Ongoing"
        booking.save()
        messages.success(request, "Ride started!")
    return redirect("dashboard:admin_dashboard" if request.user.is_staff else "bookings:user_bookings")

@login_required
def ride_end(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.user == booking.user or request.user.is_staff:
        booking.status = "Completed"
        booking.save()
        messages.success(request, "Ride completed!")
    return redirect("dashboard:admin_dashboard" if request.user.is_staff else "bookings:user_bookings")
@login_required(login_url='login')
def booking_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        payment_option = request.POST.get("payment_option")
        if payment_option:
            if payment_option == "COD":
                booking.payment_status = "Pending"
            else:
                booking.payment_status = "Paid"  # If online payment is simulated
            booking.status = "Confirmed"
            booking.save()
            messages.success(request, "Payment successful and booking confirmed!")
            return redirect("bookings:booking_confirm", booking_id=booking.id)
        else:
            messages.error(request, "Please select a payment method.")

    return render(request, "bookings/payment.html", {"booking": booking})
