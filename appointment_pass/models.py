from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

class UserDetails(AbstractUser):
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        Group,
        related_name="userdetails_groups",  # Unique related_name to prevent conflict
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userdetails_permissions",  # Unique related_name to prevent conflict
        blank=True
    )


class AppointmentDetails(models.Model):
    date = models.DateField(default=timezone.now)  # Uses the current date
    time = models.CharField(unique=True, default="12:00 AM", max_length=10)  # Uses a valid default time
    name = models.CharField(max_length=200, default="Unknown")  # Provide a sensible default

    def __str__(self):
        return f"Appointment of {self.name}"