from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from .serializer import RegisterSerializer, AppointmentDetailsSerializers
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AppointmentDetails
from datetime import datetime


User = get_user_model()


def home(request):
    return JsonResponse({"message": "Django backend is running!"})


@api_view(['POST'])
def user_register(request):
    data = request.data
    # Required fields validation
    required_fields = ["username", "name", "dob", "phone", "email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    username = data["username"]
    name = data["name"]
    dob = data["dob"]
    phone = data["phone"]
    email = data["email"]
    password = data["password"]
    # Check if the username or email already exists
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)
    # Create new user
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = name  # Store the full name in the first_name field
    user.save()
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def UserLogin(request):
    userName = request.data.get('username')
    password = request.data.get('password')
    if not userName or not password:
        return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=userName, password=password)
    if user is not None:
        login(request, user)
        return redirect('/', status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def UserLogout(request):
    logout(request)
    return redirect('/', status=status.HTTP_200_OK)


@api_view(['GET'])
def booking(request): #to display all the bookings of a user/ a perticular day
    booking_records = AppointmentDetails.objects.all()  # Get all records
    serializer = AppointmentDetailsSerializers(booking_records, many=True)  # Serialize multiple records
    return Response(serializer.data)


@api_view(['POST'])
def bookSlot(request):
    slot = request.data.get('value')  # Example: "4.30PM"
    name = request.data.get('userName')  # Get user ID from request
    date = request.data.get('dateOfApp')
    if not slot:
        return Response({'error': 'No time slot provided!'}, status=status.HTTP_400_BAD_REQUEST)
    # Check if the slot is already booked
    if AppointmentDetails.objects.get.all(date=date):
        if AppointmentDetails.objects.filter(time=slot).exists():
            return Response({'error': 'This time slot is already booked!'}, status=status.HTTP_400_BAD_REQUEST)
    # Create database entry with user ID
    AppointmentDetails.objects.create(time=slot, name=name, date=date)
    return Response({'message': 'Slot booking successful'}, status=status.HTTP_200_OK)