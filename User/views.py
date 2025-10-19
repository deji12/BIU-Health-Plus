from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User
from django.contrib.auth import authenticate
from .serializers import StudentSerializer

@api_view(['POST'])
def register_student(request):

    matric_number = request.data.get('matric_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    serial_number = request.data.get('serial_number')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if not (matric_number and first_name and last_name and password and confirm_password):
        return Response({
            "status": False,
            "message": "All fields are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(matric_number=matric_number).exists():
        return Response({
            "status": False,
            "message": "A user with this matric number exists"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not (password == confirm_password):
        return Response({
            "status": False,
            "message": "Passwords do not match"
        }, status=status.HTTP_400_BAD_REQUEST)

    new_user = User.objects.create_user(
        matric_number = matric_number,
        first_name = first_name,
        last_name = last_name,
    )

    if not serial_number:
        last_created_user = User.objects.first()
        serial_number = last_created_user.serial_number
   
    new_user.serial_number = serial_number
    new_user.save()

    serializer = StudentSerializer(new_user)
    response = {
        "status": True,
        "message": "Account created successfully",
        "user": serializer.data,
        "tokens": new_user.auth_tokens()
    }
    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    
    matric_number = request.data.get('matric_number')
    password = request.data.get('password')

    if not (matric_number and password):
        return Response({
            "status": False,
            "message": "matric number and password are required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=matric_number, password=password)

    if user is None:
        return Response({
            "status": False,
            "message": "Invalid login credentials."
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            "status": False,
            "message": "Account is deactivated"
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = StudentSerializer(user)
    return Response({
        "status": True,
        "message": "Login successful",
        "data": {
            "user": serializer.data,
            "tokens": user.auth_tokens()
        }
    }, status=status.HTTP_200_OK)