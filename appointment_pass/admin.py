from django.contrib import admin
from . models import UserDetails, AppointmentDetails

# Register your models here.
admin.site.register(UserDetails)
admin.site.register(AppointmentDetails)