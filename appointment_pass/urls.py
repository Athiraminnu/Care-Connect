from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_Register, name='register'),  # Corrected: Removed '/'
]
