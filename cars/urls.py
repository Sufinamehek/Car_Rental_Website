# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.car_list, name='car_list'),
#     #path('book/<int:id>/', views.book_car, name='book_car'),
# ]
from django.urls import path
from .views import car_list, cancel_booking

urlpatterns = [
    path('', car_list, name='car_list'),
    path('booking/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),

]
