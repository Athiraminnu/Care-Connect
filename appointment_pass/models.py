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
    bookingId = models.OneToOneField(
        UserDetails,  # Reference the UserDetails model
        on_delete=models.CASCADE,  # Deletes appointment if the user is deleted
        primary_key=True  # This makes bookingId the primary key
    )
    date = models.DateField(max_length=10, blank=False, null=False)
    time = models.TimeField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"Appointment of {self.bookingId.username}"
