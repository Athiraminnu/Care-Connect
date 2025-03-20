from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_register/', views.user_register, name='register'),
    path('login', views.UserLogin, name='login'),
    path('logout', views.UserLogout, name='logout'),
    path('bookings', views.booking, name='booking'),
    path('book/', views.bookSlot, name='bookSlot'),
    path('viewappointments/', views.appointments, name='viewappointments'),
    path('myappointments/', views.myAppointments, name='viewmyappointments'),
    path('cancel/', views.cancelMyAppointment, name='cancelmyappointment'),
]
