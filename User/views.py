from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User
from django.contrib.auth import authenticate
from .serializers import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="post",
    tags=["Auth"],
    operation_summary="Register a new student account",
    operation_description="""
    Registers a new student account using matric number, name, and password.

    **Notes for Frontend:**
    - `matric_number` must be unique.
    - All fields are required.
    - `confirm_password` must match `password`.
    - On success, this endpoint returns the student's details and authentication tokens (JWT access & refresh).

    **Authentication:** Not required.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["matric_number", "first_name", "last_name", "password", "confirm_password"],
        properties={
            "matric_number": openapi.Schema(type=openapi.TYPE_STRING, description="Unique matric number of the student."),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name of the student."),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name of the student."),
            "serial_number": openapi.Schema(type=openapi.TYPE_INTEGER, description="Student’s serial number (optional)."),
            "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Student's password."),
            "confirm_password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Must match the password."),
        },
        example={
            "matric_number": "CSC/20/1234",
            "first_name": "John",
            "last_name": "Doe",
            "serial_number": 56,
            "password": "secret123",
            "confirm_password": "secret123"
        }
    ),
    responses={
        201: openapi.Response(
            description="Student registered successfully",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Account created successfully",
                    "user": {
                        "matric_number": "CSC/20/1234",
                        "first_name": "John",
                        "middle_name": "",
                        "last_name": "Doe",
                        "user_type": "student",
                        "serial_number": 56,
                        "year_of_admission": 2025,
                        "profile_image": "https://res.cloudinary.com/health-plus/user_profile_images/default.png",
                        "date_joined": "2025-10-19T12:34:56Z"
                    },
                    "tokens": {
                        "access": "eyJ0eXAiOiJKV1QiLCJh...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": False,
                    "message": "All fields are required"
                }
            }
        ),
        401: openapi.Response(
            description="User with matric number already exists",
            examples={
                "application/json": {
                    "status": False,
                    "message": "A user with this matric number exists"
                }
            }
        ),
        422: openapi.Response(
            description="Password mismatch error",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Passwords do not match"
                }
            }
        )
    }
)
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

@swagger_auto_schema(
    method="post",
    tags=["Auth"],
    operation_summary="Login a user",
    operation_description="""
    Logs in a user using their matric number and password.

    **Notes for Frontend:**
    - Returns user details and JWT access & refresh tokens on success.
    - Account must be active to log in.
    - Invalid credentials return `401 Unauthorized`.

    **Authentication:** Not required.
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["matric_number", "password"],
        properties={
            "matric_number": openapi.Schema(type=openapi.TYPE_STRING, description="Matric number of the user."),
            "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description="Account password."),
        },
        example={
            "matric_number": "CSC/20/1234",
            "password": "secret123"
        }
    ),
    responses={
        200: openapi.Response(
            description="Login successful",
            examples={
                "application/json": {
                    "status": True,
                    "message": "Login successful",
                    "data": {
                        "user": {
                            "matric_number": "CSC/20/1234",
                            "first_name": "John",
                            "middle_name": "",
                            "last_name": "Doe",
                            "user_type": "student",
                            "serial_number": 56,
                            "year_of_admission": 2025,
                            "profile_image": "https://res.cloudinary.com/health-plus/user_profile_images/default.png",
                            "date_joined": "2025-10-19T12:34:56Z"
                        },
                        "tokens": {
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        }
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Missing fields",
            examples={
                "application/json": {
                    "status": False,
                    "message": "matric number and password are required"
                }
            }
        ),
        401: openapi.Response(
            description="Invalid credentials",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Invalid login credentials."
                }
            }
        ),
        403: openapi.Response(
            description="Inactive account",
            examples={
                "application/json": {
                    "status": False,
                    "message": "Account is deactivated"
                }
            }
        )
    }
)
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