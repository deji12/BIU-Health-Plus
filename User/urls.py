from django.urls import path
from .views import (
    register_student, login_user, 
    register_staff
)

app_name = 'user'

BASE_URL = app_name

urlpatterns = [
    path(f'{BASE_URL}/register/student/', register_student, name='register_student'),
    path(f'{BASE_URL}/login/', login_user, name='login_user'),

    path(f'{BASE_URL}/register/staff/', register_staff, name='register_staff'),
]