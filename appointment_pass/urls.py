from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line
    path('user_register/', views.user_register, name='register'),  # Corrected: Removed '/'
    path('login', views.UserLogin, name='login'),
    path('logout', views.UserLogout, name='logout'),

]
