# from django.urls import path
# from . import views

# urlpatterns = [
#     path('book/<int:car_id>/', views.book_car, name='book_car'),
# ]
from django.urls import path
from . import views
  

app_name = 'bookings'
urlpatterns = [
    path('', views.bookings_index, name='bookings_index'),
    path('book_car/<int:car_id>/', views.book_car, name='book_car'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('booking_confirm/<int:booking_id>/', views.booking_confirm, name='booking_confirm'),  # ✅ Add this
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path("payment/<int:booking_id>/", views.payment_method, name="payment_method"),
#     path("ride_start/<int:booking_id>/", views.ride_start, name="ride_start"),
#     path("ride_end/<int:booking_id>/", views.ride_end, name="ride_end"),
 ]

