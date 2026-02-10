from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings    
from .views import home
from cars import views as car_views  # adjust if your login view is elsewhere
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cars/', include('cars.urls')),  # <-- Car listing
    path('bookings/', include('bookings.urls')),
    path('login/', car_views.login_view, name='login'),  # <--- add this
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),  
    path('signup/', car_views.signup_view, name='signup'),  # <- name must be 'signup'
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

# project/urls.py




# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('cars/', include('cars.urls')),
#     path('accounts/', include('accounts.urls')),
#     path('bookings/', include('bookings.urls')),
#     path('dashboard/', include('dashboard.urls')),
# ]


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)