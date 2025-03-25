from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
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
    print("Request Data:", request.data)  # Debugging line
    userName = request.data.get('username')
    password = request.data.get('password')

    if not userName or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=userName, password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def UserLogout(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)

@api_view(['GET'])
def booking(request):
    booking_records = AppointmentDetails.objects.all()
    serializer = AppointmentDetailsSerializers(booking_records, many=True)
    return Response(serializer.data)


@api_view(['POST', 'GET'])  # Ensure GET is included
def bookSlot(request):
    if request.method == 'GET':
        date = request.GET.get('dateOfApp')
        if not date:
            return Response({"error": "Date parameter is required"}, status=400)

        booked_slots = AppointmentDetails.objects.filter(date=date)
        serializer = AppointmentDetailsSerializers(booked_slots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        slot = request.data.get('value')
        name = request.data.get('userName')
        date = request.data.get('dateOfApp')

        if not slot or not date:
            return Response({'error': "Missing time or date"}, status=status.HTTP_400_BAD_REQUEST)

        if AppointmentDetails.objects.filter(date=date, time=slot).exists():
            return Response({'error': 'This time slot is already booked!'}, status=status.HTTP_400_BAD_REQUEST)

        # Create appointment
        AppointmentDetails.objects.create(time=slot, name=name, date=date)

        return Response({'message': 'Slot booking successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def appointments(request):
    if request.method == 'GET':
        date = request.GET.get('date', None)
        if date:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d").date()  # Ensure YYYY-MM-DD format
                allAppointments = AppointmentDetails.objects.filter(date=formatted_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        else:
            allAppointments = AppointmentDetails.objects.all()
        if allAppointments:
            serializer = AppointmentDetailsSerializers(allAppointments, many=True)
        else:
            return Response({'msg': 'No Data Found !'})
        return Response(serializer.data)


@api_view(['GET'])
def myAppointments(request):
    if request.method == 'GET':
        username = request.headers.get('UserInfo')
        appointments = AppointmentDetails.objects.filter(name=username)
        if not appointments.exists():
            return Response({"message": "No Appointments Found!"}, status=404)
        serialized_data = AppointmentDetailsSerializers(appointments, many=True).data
        return Response(serialized_data, status=200)


@api_view(['POST'])
def cancelMyAppointment(request):
    time = request.data.get('cancelTime')
    date = request.data.get('cancelDate')
    if not time or not date:
        return Response({'error': "Missing cancelTime or cancelDate"}, status=400)
    deleteAppointment = AppointmentDetails.objects.filter(date=date, time=time)
    if deleteAppointment.exists():
        deleteAppointment.delete()
        return Response({'message' : "Appointment cancelled sucessfully !"}, status=200)
    else:
        return Response({"message": "No matching Appointment found !!"}, status=404)